#!/usr/bin/env python3
"""Isolated EOS packet probe for the explicitly authorized SAI TUI lab.

Run as root on ixp-lab-eos1. Opens sockets in the two disposable test VRFs
(or the default namespace for direct Ethernet9/2 transmission). Reports real
received marker packets, including MAC rewrite and IP TTL/hop limit. Does not
change routes, neighbours, interface configuration or counters. No dependencies.
"""
import argparse
import ctypes
import ipaddress
import json
import os
import select
import socket
import struct
import time


def checksum(data):
    if len(data) & 1:
        data += b"\0"
    total = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    while total >> 16:
        total = (total & 65535) + (total >> 16)
    return (~total) & 65535


def mac(text):
    data = bytes.fromhex(text.replace(":", ""))
    if len(data) != 6:
        raise ValueError("MAC must contain 6 octets")
    return data


def mac_text(data):
    return ":".join("%02x" % b for b in data)


def packet(args, nonce, sequence):
    source = ipaddress.ip_address(args.src_ip)
    target = ipaddress.ip_address(args.dst_ip)
    if source.version != target.version:
        raise ValueError("IP families differ")
    payload = b"SAITUI:" + nonce + struct.pack("!I", sequence) + b" verified on EOS"
    udp = struct.pack("!HHHH", 49000, 49001, 8 + len(payload), 0) + payload
    if source.version == 4:
        pseudo = source.packed + target.packed + struct.pack("!BBH", 0, 17, len(udp))
        ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(udp), sequence, 0, 64, 17, 0,
                         source.packed, target.packed)
        ip = ip[:10] + struct.pack("!H", checksum(ip)) + ip[12:]
        ether_type = 0x0800
    else:
        pseudo = source.packed + target.packed + struct.pack("!I3xB", len(udp), 17)
        ip = struct.pack("!IHBB16s16s", 6 << 28, len(udp), 17, 64, source.packed, target.packed)
        ether_type = 0x86dd
    udp = udp[:6] + struct.pack("!H", checksum(pseudo + udp) or 65535) + udp[8:]
    ether = mac(args.dst_mac) + mac(args.src_mac)
    if args.vlan:
        ether += struct.pack("!HH", 0x8100, args.vlan)
    frame = ether + struct.pack("!H", ether_type) + ip + udp
    return frame.ljust(60, b"\0")


def parse(frame, marker):
    at = frame.find(marker)
    if at < 0 or len(frame) < at + len(marker) + 4:
        return None
    result = {"src_mac": mac_text(frame[6:12]), "dst_mac": mac_text(frame[:6]),
              "sequence": struct.unpack("!I", frame[at + len(marker):at + len(marker) + 4])[0]}
    ether_type = struct.unpack("!H", frame[12:14])[0]
    offset = 14
    if ether_type == 0x8100:
        result["vlan"] = struct.unpack("!H", frame[14:16])[0] & 4095
        ether_type = struct.unpack("!H", frame[16:18])[0]
        offset += 4
    if ether_type == 0x0800:
        result.update(family="ipv4", ttl=frame[offset + 8],
                      src_ip=socket.inet_ntop(socket.AF_INET, frame[offset + 12:offset + 16]),
                      dst_ip=socket.inet_ntop(socket.AF_INET, frame[offset + 16:offset + 20]))
    elif ether_type == 0x86dd:
        result.update(family="ipv6", ttl=frame[offset + 7],
                      src_ip=socket.inet_ntop(socket.AF_INET6, frame[offset + 8:offset + 24]),
                      dst_ip=socket.inet_ntop(socket.AF_INET6, frame[offset + 24:offset + 40]))
    else:
        return None
    return result


def open_socket(namespace, interface, original):
    allowed_ns = {"default", "ns-SAI-TUI-A", "ns-SAI-TUI-B"}
    if namespace not in allowed_ns or interface not in {"et9_1", "et9_2", "vlan3901"}:
        raise ValueError("probe is limited to the documented isolated lab endpoints")
    libc = ctypes.CDLL(None, use_errno=True)
    with open("/var/run/netns/" + namespace) as handle:
        if libc.setns(handle.fileno(), 0x40000000):
            raise OSError(ctypes.get_errno(), "setns " + namespace)
    try:
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
        sock.bind((interface, 0))
        sock.setblocking(False)
    finally:
        if libc.setns(original, 0x40000000):
            raise OSError(ctypes.get_errno(), "restore namespace")
    return sock


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["tx-ns", "tx-if", "rx-ns", "rx-if", "src-ip", "dst-ip"]:
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--src-mac", default="02:00:00:00:a0:01")
    parser.add_argument("--dst-mac", default="74:83:ef:3f:2c:fd")
    parser.add_argument("--vlan", type=int, default=0)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seconds", type=float, default=2)
    args = parser.parse_args()
    if not 1 <= args.count <= 10000 or not 0 < args.seconds <= 10 or args.vlan not in [0, 3901]:
        parser.error("count/duration/VLAN exceeds isolated probe limits")
    for ip in [args.src_ip, args.dst_ip]:
        address = ipaddress.ip_address(ip)
        allowed = ipaddress.ip_network("198.18.0.0/15" if address.version == 4 else "fd00::/8")
        if address not in allowed:
            parser.error("probe IPs must be within the isolated test ranges")
    nonce = os.urandom(8)
    marker = b"SAITUI:" + nonce
    with open("/proc/self/ns/net") as original:
        receiver = open_socket(args.rx_ns, args.rx_if, original.fileno())
        sender = open_socket(args.tx_ns, args.tx_if, original.fileno())
    with receiver, sender:
        for sequence in range(args.count):
            sender.send(packet(args, nonce, sequence))
        deadline = time.monotonic() + args.seconds
        received = {}
        while time.monotonic() < deadline and len(received) < args.count:
            if not select.select([receiver], [], [], max(0, deadline - time.monotonic()))[0]:
                break
            frame, source = receiver.recvfrom(65536)
            if source[2] == 4:  # PACKET_OUTGOING is not external reception.
                continue
            observed = parse(frame, marker)
            if observed is not None:
                received[observed["sequence"]] = observed
    print(json.dumps({"sent": args.count, "received": len(received), "packets": list(received.values()),
                      "tx": [args.tx_ns, args.tx_if], "rx": [args.rx_ns, args.rx_if]}, sort_keys=True))


if __name__ == "__main__":
    main()
