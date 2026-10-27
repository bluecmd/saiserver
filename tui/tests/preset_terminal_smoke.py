#!/usr/bin/env python3
"""Real PTY + loopback Thrift test: preset loading never mutates hardware.

Uses a deliberately tiny snapshot-only server, not a switch or vendor SDK.
Usage: python3 tui/tests/preset_terminal_smoke.py tui/target/debug/sai-tui
"""
import socket
import struct
import threading
import unittest

import terminal_smoke


def string(value):
    value = value.encode()
    return struct.pack("!i", len(value)) + value


def field(kind, number, value):
    return struct.pack("!bh", kind, number) + value


def obj(kind, key, attributes):
    pairs = b"".join(string(k) + string(v) for k, v in attributes.items())
    return (field(11, 1, string(kind)) + field(11, 2, string(key))
            + field(13, 3, struct.pack("!bbi", 11, 11, len(attributes)) + pairs) + b"\0")


def snapshot():
    ports = []
    for i in range(33):
        lanes = range(4 * i + 1, 4 * i + 5) if i < 32 else [129]
        ports.append(obj("port", hex(i + 1), {
            "lanes": ",".join(map(str, lanes)),
            "speed": "100000" if i < 32 else "10000",
            "ingress_acl": "0x0", "egress_acl": "0x0",
            "egress_mirror_sessions": "", "pvid": "1",
        }))
    ports.append(obj("switch", "0x1000", {
        "src_mac": "02:00:00:00:01:01", "default_vlan": "0x1001",
        "preset_api": "1", "interface_address_backend": "enabled",
    }))
    return (field(15, 1, struct.pack("!bi", 12, len(ports)) + b"".join(ports))
            + field(15, 2, struct.pack("!bi", 11, 0)) + b"\0")


def read_exact(peer, length):
    data = b""
    while len(data) < length:
        chunk = peer.recv(length - len(data))
        if not chunk:
            raise RuntimeError("truncated Thrift request")
        data += chunk
    return data


class PresetTerminalSmoke(terminal_smoke.TerminalSmoke):
    def test_preset_review_cancel_and_local_load(self):
        calls = []
        errors = []
        stop = threading.Event()
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            listener.settimeout(0.1)

            def serve():
                try:
                    while not stop.is_set():
                        try:
                            peer, _ = listener.accept()
                        except socket.timeout:
                            continue
                        with peer:
                            peer.settimeout(2)
                            version, length = struct.unpack("!Ii", read_exact(peer, 8))
                            if version != 0x80010001 or not 0 <= length < 128:
                                raise RuntimeError("invalid binary Thrift request")
                            method = read_exact(peer, length).decode()
                            sequence = read_exact(peer, 4)
                            calls.append(method)
                            if method != "tui_snapshot":
                                raise RuntimeError(f"loading unexpectedly sent {method}")
                            if read_exact(peer, 1) != b"\0":
                                raise RuntimeError("snapshot arguments were not empty")
                            result = field(12, 0, snapshot()) + b"\0"
                            peer.sendall(struct.pack("!I", 0x80010002)
                                         + string(method) + sequence + result)
                except Exception as error:  # surface thread failures in the test
                    errors.append(error)

            thread = threading.Thread(target=serve, daemon=True)
            thread.start()
            try:
                process, master, slave, original = self.start(
                    f"127.0.0.1:{listener.getsockname()[1]}", 1000)
                import os
                self.until(master, b"Discovery refreshed")
                os.write(master, b"p\r")
                self.until(master, b"REVIEW LOCAL LOAD")
                os.write(master, b"n")
                self.until(master, b"Cancelled")
                os.write(master, b":preset show\r")
                self.until(master, b"No staged configuration")
                os.write(master, b"p\r")
                self.until(master, b"REVIEW LOCAL LOAD")
                os.write(master, b"y")
                self.until(master, b"Preset staged locally")
                os.write(master, b"a")
                self.until(master, b"REVIEW HARDWARE APPLY")
                os.write(master, b"n")
                self.until(master, b"Cancelled")
                self.assert_restored(process, master, slave, original)
            finally:
                stop.set()
                thread.join(timeout=3)
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(calls, ["tui_snapshot"])


if __name__ == "__main__":
    # Inherited terminal safety tests run too; all endpoints are loopback-only.
    unittest.main()
