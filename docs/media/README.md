# TUI screenshots and screencast replays

These assets showcase the **actual 2026-10-27 ixp-lab-sw4 session** documented
in [the live verification record](../lab-verification.md), with traffic supplied
and received by ixp-lab-eos1. No additional switch initialization or test outage
was performed to create these media files.

## Videos

| Replay | GIF preview | Full-resolution MP4 | Source snapshots |
| --- | --- | --- | --- |
| Configuration review, cancellation, confirmation and getter readback | [GIF](sai-tui-configuration.gif) | [H.264 MP4](sai-tui-configuration.mp4) | 0–6, original elapsed 2.016–12.024 s |
| Selected-port counters and traffic-rate graph | [GIF](sai-tui-counters.gif) | [H.264 MP4](sai-tui-counters.mp4) | 7–11, original elapsed 15.033–27.039 s |

**Capture fidelity:** these are replays of timestamped terminal states, not
continuous video footage. `capture_tui.py` saved snapshots immediately before
scheduled key actions during the real session. Each recorded state is held
until the next captured timestamp; the last state is frozen for one second.
The video's 12 fps encoding duplicates those held states and does not invent
intermediate terminal output. GIF timing is quantized to hundredths of a second.
The MP4s have no audio and use H.264/yuv420p with fast-start metadata.

The source [sw4-terminal-capture.json](sw4-terminal-capture.json) is a verbatim
copy of those recorded terminal cells and timestamps. Styling is reconstructed
in monochrome because this capture format retained characters, not terminal
cell colors. Unicode Braille chart characters are drawn from their actual dot
masks, avoiding missing font glyphs; no graph points or counter values are added.
The source timestamps remain visible in every rendered state.

Configuration footage includes an explicit cancel, a separate confirmation,
and actual getter output. Counter footage includes both idle observations and
the recorded 251937.4 bit/s RX observation. Separate JSON counter samples and
packet evidence remain linked from the live record. The SDK limitations and
unverified operations described there also apply to the showcased application.

## Screenshots

The README includes the [counter screen](../evidence/sw4-tui-counters.png),
[mutation review](../evidence/sw4-tui-review.png), and
[actual getter readback](../evidence/sw4-tui-readback.png). Their corresponding
`.txt` files preserve the recorded terminal characters without rasterization.

## Regenerate locally

Requires Python 3, Pillow, ffmpeg with libx264, and a monospace font. The default
font is DejaVu Sans Mono at the standard Linux path; use `--font /path/to/font.ttf`
on another platform. Regeneration needs **no Thrift server, SSH or lab access**.

From the repository root:

```sh
python3 -m venv /tmp/sai-tui-media-venv
/tmp/sai-tui-media-venv/bin/pip install Pillow
PYTHON=/tmp/sai-tui-media-venv/bin/python

$PYTHON tests/lab/render_screencast.py docs/media/sw4-terminal-capture.json \
  --output-dir docs/media --name sai-tui-configuration --first 0 --last 6 \
  --label 'sai-tui | review, cancel, confirm and getter readback | ixp-lab-sw4'

$PYTHON tests/lab/render_screencast.py docs/media/sw4-terminal-capture.json \
  --output-dir docs/media --name sai-tui-counters --first 7 --last 11 \
  --label 'sai-tui | live port counters and traffic-rate graph | ixp-lab-sw4'
```

[manifest.json](manifest.json) records source/output hashes, selected snapshot
ranges and inspected media metadata. Re-encoding with another ffmpeg or Pillow
version can change output hashes without changing the source capture.
