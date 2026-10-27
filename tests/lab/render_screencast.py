#!/usr/bin/env python3
"""Render timestamped capture_tui.py terminal snapshots as a GIF and MP4 replay.

This does not claim to recover frames between captured snapshots. Each recorded
state is held until the next timestamp; the last state is frozen for one second.
Requires Pillow and ffmpeg with libx264. No switch access or network is used.
"""
import argparse
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


def render_screen(snapshot, font, label):
    screen = snapshot["screen"]
    cell_width = font.getlength("M")
    line_height = font.size + 3
    width = math.ceil((max(map(len, screen)) * cell_width + 24) / 2) * 2
    height = math.ceil((len(screen) * line_height + 66) / 2) * 2
    image = Image.new("RGB", (width, height), (18, 22, 28))
    draw = ImageDraw.Draw(image)
    foreground = (222, 230, 235)
    draw.text((12, 9), label, font=font, fill=(134, 204, 240))
    draw.text((12, 27), f"Recorded state at +{snapshot['at']:.3f}s | timestamped terminal replay",
              font=font, fill=(157, 170, 182))
    for row, line in enumerate(screen):
        for column, character in enumerate(line):
            left, top = 12 + column * cell_width, 52 + row * line_height
            dots = ord(character) - 0x2800
            if 0 <= dots <= 255:
                # Draw the exact Unicode Braille dot mask from the capture;
                # the installed monospace font does not include these glyphs.
                for col, y, bit in [(0, 0, 0), (0, 1, 1), (0, 2, 2), (0, 3, 6),
                                    (1, 0, 3), (1, 1, 4), (1, 2, 5), (1, 3, 7)]:
                    if dots & (1 << bit):
                        x0, y0 = left + 2 + col * 4, top + 3 + y * 3
                        draw.ellipse((x0, y0, x0 + 1.5, y0 + 1.5), fill=foreground)
            else:
                draw.text((left, top), character, font=font, fill=foreground)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--first", type=int, required=True)
    parser.add_argument("--last", type=int, required=True)
    parser.add_argument("--label", default="sai-tui | live ixp-lab-sw4 session")
    parser.add_argument("--font", default="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    snapshots = json.loads(args.capture.read_text())
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.name):
        parser.error("name must contain only letters, digits, '-' or '_'")
    if not 0 <= args.first <= args.last < len(snapshots):
        parser.error("first/last must select existing snapshots")
    snapshots = snapshots[args.first:args.last + 1]
    durations = [b["at"] - a["at"] for a, b in zip(snapshots, snapshots[1:])] + [1.0]
    if any(not math.isfinite(d) or d <= 0 for d in durations):
        parser.error("snapshot timestamps must be finite and increasing")
    font = ImageFont.truetype(args.font, 14)
    images = [render_screen(snapshot, font, args.label) for snapshot in snapshots]
    if len({image.size for image in images}) != 1:
        parser.error("selected snapshots must have identical terminal dimensions")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    previews = []
    for image in images:
        height = round(image.height * 960 / image.width)
        previews.append(image.resize((960, height), Image.Resampling.LANCZOS).convert(
            "P", palette=Image.Palette.ADAPTIVE, colors=32))
    gif = args.output_dir / (args.name + ".gif")
    previews[0].save(gif, save_all=True, append_images=previews[1:],
                     duration=[max(10, round(d * 1000)) for d in durations],
                     loop=0, optimize=True, disposal=2)
    mp4 = args.output_dir / (args.name + ".mp4")
    with tempfile.TemporaryDirectory(prefix="sai-tui-replay-") as temporary:
        directory = Path(temporary)
        lines = ["ffconcat version 1.0"]
        for i, (image, duration) in enumerate(zip(images, durations)):
            path = directory / f"frame-{i:03}.png"
            image.save(path)
            lines += [f"file '{path.as_posix()}'", f"duration {duration:.6f}"]
        lines.append(f"file '{path.as_posix()}'")
        playlist = directory / "frames.ffconcat"
        playlist.write_text("\n".join(lines) + "\n")
        subprocess.run([
            args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-f", "concat", "-safe", "0", "-i", str(playlist),
            "-t", f"{sum(durations):.6f}", "-vf", "fps=12",
            "-c:v", "libx264", "-preset", "slow", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4),
        ], check=True)
    print(json.dumps({"gif": str(gif), "mp4": str(mp4),
                      "recorded_states": len(snapshots), "duration_seconds": sum(durations),
                      "source_range_seconds": [snapshots[0]["at"], snapshots[-1]["at"]],
                      "last_state_freeze_seconds": 1.0}, indent=2))


if __name__ == "__main__":
    main()
