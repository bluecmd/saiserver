#!/usr/bin/env python3
"""Record a real terminal session with bounded, reproducible keyboard input.

Example (run from the repository root):
  python3 tests/lab/capture_tui.py --output .lab/tui.ansi --actions .lab/keys.json \
      -- ssh -tt ixp-lab-sw4.local.sonix.network /home/bluecmd/saitui-lab/sai-tui

Actions JSON: [{"at": 2, "keys": "\\t"}, {"at": 5, "keys": "q"}].
Optional `pyte` enables readable screen snapshots. No shell is invoked locally.
Only the explicitly supplied command is started/stopped. This is a lab helper,
not an unattended switch-configuration tool.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import termios
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--actions", required=True, type=Path)
    parser.add_argument("--seconds", type=float, default=20)
    parser.add_argument("--columns", type=int, default=140)
    parser.add_argument("--rows", type=int, default=42)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or not 0 < args.seconds <= 300:
        parser.error("supply a command and a duration in (0, 300]")
    actions = sorted(json.loads(args.actions.read_text()), key=lambda item: item["at"])
    if any(not 0 <= item["at"] < args.seconds or not isinstance(item["keys"], str)
           for item in actions):
        parser.error("actions must have times within the recording and string keys")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ,
                struct.pack("HHHH", args.rows, args.columns, 0, 0))
    env = dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor")
    process = subprocess.Popen(command, stdin=slave, stdout=slave, stderr=slave,
                               start_new_session=True, env=env)
    os.close(slave)
    screen = stream = None
    try:
        import pyte
        screen = pyte.Screen(args.columns, args.rows)
        stream = pyte.ByteStream(screen)
    except ImportError:
        pass
    started = time.monotonic()
    next_action = 0
    snapshots = []
    timed_out = False
    try:
        with args.output.open("wb") as log:
            while process.poll() is None:
                elapsed = time.monotonic() - started
                if elapsed >= args.seconds:
                    timed_out = True
                    break
                while next_action < len(actions) and actions[next_action]["at"] <= elapsed:
                    if screen is not None:
                        snapshots.append({"at": round(elapsed, 3), "screen": screen.display[:]})
                    os.write(master, actions[next_action]["keys"].encode())
                    next_action += 1
                if select.select([master], [], [], min(0.1, args.seconds - elapsed))[0]:
                    try:
                        data = os.read(master, 65536)
                    except OSError:
                        break
                    if not data:
                        break
                    log.write(data)
                    log.flush()
                    if stream is not None:
                        stream.feed(data)
            # Drain the terminal without an unbounded read after the child exits.
            while select.select([master], [], [], 0)[0]:
                try:
                    data = os.read(master, 65536)
                except OSError:
                    break
                if not data:
                    break
                log.write(data)
                if stream is not None:
                    stream.feed(data)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        os.close(master)
    if screen is not None:
        snapshots.append({"at": round(time.monotonic() - started, 3), "screen": screen.display[:]})
        args.output.with_suffix(".screens.json").write_text(json.dumps(snapshots, indent=2) + "\n")
    result = {"command": command, "exit_code": process.returncode,
              "timed_out": timed_out, "actions_sent": next_action,
              "transcript": str(args.output), "screen_snapshots": len(snapshots)}
    args.output.with_suffix(".result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 124 if timed_out else process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
