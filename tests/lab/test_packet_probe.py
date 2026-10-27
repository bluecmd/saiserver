#!/usr/bin/env python3
"""Offline checks for the exact marker-frame generator used in live tests."""
import ipaddress
from pathlib import Path
import struct
import subprocess
import sys
from types import SimpleNamespace
import unittest

import eos_packet_probe as probe


class PacketProbeTests(unittest.TestCase):
    def test_rfc_checksum_and_odd_length(self):
        self.assertEqual(probe.checksum(bytes.fromhex(
            "45000073000040004011b861c0a80001c0a800c7")), 0)
        self.assertEqual(probe.checksum(b"\x01"), 0xfeff)
        self.assertEqual(probe.checksum(b""), 0xffff)

    def test_both_families_tagging_and_udp_checksums(self):
        for src, dst in [("198.18.200.1", "198.18.200.2"),
                         ("fd00:3901::1", "fd00:3901::2")]:
            for vlan in [0, 3901]:
                with self.subTest(src=src, vlan=vlan):
                    args = SimpleNamespace(src_ip=src, dst_ip=dst, vlan=vlan,
                                           src_mac="02:00:00:00:a0:01",
                                           dst_mac="74:83:ef:3f:2c:fd")
                    nonce = b"12345678"
                    frame = probe.packet(args, nonce, 42)
                    observed = probe.parse(frame, b"SAITUI:" + nonce)
                    self.assertEqual(observed["sequence"], 42)
                    self.assertEqual(observed["ttl"], 64)
                    self.assertEqual(observed["src_ip"], src)
                    self.assertEqual(observed["dst_ip"], dst)
                    self.assertEqual(observed.get("vlan", 0), vlan)
                    self.assertEqual(observed["src_mac"], args.src_mac)
                    self.assertEqual(observed["dst_mac"], args.dst_mac)
                    offset = 18 if vlan else 14
                    source, target = ipaddress.ip_address(src), ipaddress.ip_address(dst)
                    if source.version == 4:
                        self.assertEqual(probe.checksum(frame[offset:offset + 20]), 0)
                        length = struct.unpack("!H", frame[offset + 2:offset + 4])[0] - 20
                        udp = frame[offset + 20:offset + 20 + length]
                        pseudo = source.packed + target.packed + struct.pack("!BBH", 0, 17, length)
                    else:
                        length = struct.unpack("!H", frame[offset + 4:offset + 6])[0]
                        udp = frame[offset + 40:offset + 40 + length]
                        pseudo = source.packed + target.packed + struct.pack("!I3xB", length, 17)
                    self.assertEqual(probe.checksum(pseudo + udp), 0)
                    self.assertIsNone(probe.parse(frame, b"different marker"))

    def test_bad_mac_and_mixed_family(self):
        with self.assertRaises(ValueError):
            probe.mac("00:11")
        with self.assertRaises(ValueError):
            probe.packet(SimpleNamespace(src_ip="198.18.200.1", dst_ip="fd00::1"), b"nonce", 0)

    def test_namespace_and_interface_guards_without_privileges(self):
        for ns, interface in [("unrelated", "et9_1"), ("default", "eth0")]:
            with self.assertRaises(ValueError):
                probe.open_socket(ns, interface, -1)

    def test_cli_rejects_out_of_scope_ip_before_opening_sockets(self):
        result = subprocess.run([
            sys.executable, str(Path(probe.__file__)), "--tx-ns", "default",
            "--tx-if", "et9_1", "--rx-ns", "default", "--rx-if", "et9_2",
            "--src-ip", "203.0.113.1", "--dst-ip", "198.18.200.2",
        ], capture_output=True, text=True, timeout=3)
        self.assertEqual(result.returncode, 2)
        self.assertIn("isolated test ranges", result.stderr)


if __name__ == "__main__":
    unittest.main()
