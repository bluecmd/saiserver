#!/usr/bin/env python3
"""Unix PTY smoke tests; no lab. Usage: python3 tui/tests/terminal_smoke.py [binary]."""
import errno
import fcntl
import os
from pathlib import Path
import pty
import selectors
import signal
import socket
import struct
import subprocess
import sys
import termios
import time
import unittest

BINARY = str(Path(sys.argv.pop(1) if len(sys.argv) > 1 else "tui/target/debug/sai-tui").resolve())


class TerminalSmoke(unittest.TestCase):
    def start(self, endpoint, timeout):
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 35, 120, 0, 0))
        original = termios.tcgetattr(slave)
        process = subprocess.Popen(
            [BINARY, "--endpoint", endpoint, "--timeout-ms", str(timeout)],
            stdin=slave, stdout=slave, stderr=slave, start_new_session=True,
            env={**os.environ, "TERM": "xterm-256color"},
        )
        self.addCleanup(self.cleanup, process, master, slave)
        return process, master, slave, original

    @staticmethod
    def cleanup(process, master, slave):
        if process.poll() is None:
            process.kill()
            process.wait(timeout=2)
        os.close(master)
        os.close(slave)

    def until(self, master, needle, seconds=4):
        data = b""
        end = time.monotonic() + seconds
        with selectors.DefaultSelector() as selector:
            selector.register(master, selectors.EVENT_READ)
            while time.monotonic() < end:
                if not selector.select(max(0, end - time.monotonic())):
                    break
                try:
                    data += os.read(master, 65536)
                except OSError as error:
                    if error.errno == errno.EIO:
                        break
                    raise
                if needle in data:
                    return data
        self.fail(f"did not see {needle!r}; screen bytes: {data!r}")

    def assert_restored(self, process, master, slave, original):
        start = time.monotonic()
        os.write(master, b"q")
        self.assertEqual(process.wait(timeout=2), 0)
        self.assertLess(time.monotonic() - start, 1)
        self.assertEqual(termios.tcgetattr(slave), original)
        # Alternate screen leave sequence (other bytes may already be buffered).
        self.until(master, b"\x1b[?1049l")

    def test_initial_failure_stays_in_ui_and_restores_terminal(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            endpoint = f"127.0.0.1:{listener.getsockname()[1]}"
        process, master, slave, original = self.start(endpoint, 100)
        self.until(master, b"Press r to reconnect")
        self.assertIsNone(process.poll())
        self.assert_restored(process, master, slave, original)

    def test_quit_does_not_wait_for_stalled_rpc(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            listener.settimeout(3)
            process, master, slave, original = self.start(
                f"127.0.0.1:{listener.getsockname()[1]}", 5000
            )
            peer, _ = listener.accept()
            with peer:
                self.until(master, b"RPC in progress")
                self.assert_restored(process, master, slave, original)

    def test_signal_failure_also_restores_terminal(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            endpoint = f"127.0.0.1:{listener.getsockname()[1]}"
        process, master, slave, original = self.start(endpoint, 100)
        self.until(master, b"Press r to reconnect")
        process.send_signal(signal.SIGTERM)
        self.assertNotEqual(process.wait(timeout=2), 0)
        self.assertEqual(termios.tcgetattr(slave), original)
        self.until(master, b"\x1b[?1049l")

    def test_reconnect_prompt_accepts_refresh(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            endpoint = f"127.0.0.1:{listener.getsockname()[1]}"
            process, master, slave, original = self.start(endpoint, 100)
            self.until(master, b"Press r to reconnect")
            listener.listen()
            listener.settimeout(3)
            os.write(master, b"r")
            peer, _ = listener.accept()
            with peer:
                # Accept proves refresh actually reconnected after the failure.
                self.assert_restored(process, master, slave, original)


if __name__ == "__main__":
    unittest.main()
