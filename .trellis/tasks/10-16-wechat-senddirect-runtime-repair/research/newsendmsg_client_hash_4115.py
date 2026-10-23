"""Offline unsigned hash from 0x33fcc -> 0x9ebf8, used for item field 5.

The upstream string helper has the retained native label GetSendClientId.
This module hashes caller-supplied synthetic bytes; it does not generate or
read a live client ID. Native tail bytes are signed for remainders 1 and 3.
"""
from __future__ import annotations


def client_hash(data: bytes) -> int:
    """Port the frozen ARM64 leaf with explicit 32-bit wraparound."""
    if type(data) is not bytes:
        raise TypeError('client ID input must be immutable bytes')
    if not data or len(data) >= 0x80000000:
        return 0
    mask = 0xFFFFFFFF
    value = len(data)
    blocks, remainder = divmod(len(data), 4)
    for index in range(blocks):
        offset = index * 4
        value = (value + int.from_bytes(data[offset:offset + 2], 'little')) & mask
        mixed = (int.from_bytes(data[offset + 2:offset + 4], 'little') << 11) ^ (value << 16)
        value = (value ^ mixed) & mask
        value = (value + (value >> 11)) & mask
    tail = data[blocks * 4:]
    if remainder == 1:
        value = (value + int.from_bytes(tail, 'little', signed=True)) & mask
        value = (value ^ (value << 10)) & mask
        value = (value + (value >> 1)) & mask
    elif remainder == 2:
        value = (value + int.from_bytes(tail, 'little')) & mask
        value = (value ^ (value << 11)) & mask
        value = (value + (value >> 17)) & mask
    elif remainder == 3:
        value = (value + int.from_bytes(tail[:2], 'little')) & mask
        signed_last = int.from_bytes(tail[2:], 'little', signed=True)
        value = (value ^ (value << 16) ^ (signed_last << 18)) & mask
        value = (value + (value >> 11)) & mask
    value = (value ^ (value << 3)) & mask
    value = (value + (value >> 5)) & mask
    value = (value ^ (value << 4)) & mask
    value = (value + (value >> 17)) & mask
    value = (value ^ (value << 25)) & mask
    return (value + (value >> 6)) & mask
