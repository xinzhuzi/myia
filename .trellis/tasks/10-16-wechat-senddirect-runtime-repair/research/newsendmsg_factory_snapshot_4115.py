"""Bounded injected reader for one native factory entry; no debugger or I/O.

Source: 0x30c2c1c x0/x1/x2, 0x465da58, 0x465d024 and 0x4f37c94.
Output contains digests/lengths and numbered integers, never string payloads.
"""
from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping


def inspect_factory(read: Callable[[int, int], bytes], base: int,
                    registers: Mapping[str, int], service: int) -> dict:
    """Capture exactly one item. The reader must also enforce a time deadline."""
    if type(base) is not int or base < 4096 or base % 4096:
        raise ValueError('invalid base')
    if registers['x0'] != service:
        raise ValueError('factory service differs from verified identity')
    reads = total = 0

    def take(address: int, length: int) -> bytes:
        nonlocal reads, total
        if type(address) is not int or address < 4096 or not 0 < length <= 4096:
            raise ValueError('invalid bounded read')
        reads += 1
        total += length
        if reads > 48 or total > 12288:
            raise ValueError('snapshot budget exceeded')
        raw = read(address, length)
        if type(raw) is not bytes or len(raw) != length:
            raise ValueError('short snapshot read')
        return raw

    def pointer(raw: bytes) -> int:
        value = int.from_bytes(raw, 'little')
        if value < 4096 or value % 8:
            raise ValueError('invalid pointer; no masking or scan')
        return value

    def string(address: int, bound: int) -> dict:
        header = take(address, 24)
        if header[23] & 0x80:
            size = int.from_bytes(header[8:16], 'little')
            capacity = int.from_bytes(header[16:24], 'little') & 0x7FFFFFFFFFFFFFFF
            if size > bound or size >= capacity:
                raise ValueError('long string exceeds allocation bound')
            payload = take(pointer(header[:8]), size) if size else b''
        else:
            size = header[23]
            if size > 22 or size > bound:
                raise ValueError('invalid short string length')
            payload = header[:size]
        return {'bytes': size, 'sha256': hashlib.sha256(payload).hexdigest()}

    body = take(registers['x1'], 48)
    if int.from_bytes(body[:8], 'little') != base + 0x9E91DF8:
        raise ValueError('body vtable mismatch')
    count = int.from_bytes(body[16:20], 'little', signed=True)
    allocated = int.from_bytes(body[20:24], 'little', signed=True)
    capacity = int.from_bytes(body[24:28], 'little', signed=True)
    declared = int.from_bytes(body[32:36], 'little')
    if count != 1 or not 1 <= allocated <= capacity <= 1024 or declared != 1:
        raise ValueError('only a single declared/actual item is permitted')
    if not int.from_bytes(body[40:44], 'little') & 1:
        raise ValueError('outer required field absent')
    item = take(pointer(take(pointer(body[8:16]), 8)), 56)
    if int.from_bytes(item[:8], 'little') != base + 0x9E91D80:
        raise ValueError('item vtable mismatch')
    mask = int.from_bytes(item[52:56], 'little')
    if mask & 0x1D != 0x1D:
        raise ValueError('item required fields absent')
    wrapper = take(pointer(item[8:16]), 24)
    if int.from_bytes(wrapper[:8], 'little') != base + 0x9ECA390:
        raise ValueError('wrapper vtable mismatch')
    nested_mask = int.from_bytes(wrapper[20:24], 'little')
    fields = {
        '1': string(pointer(wrapper[8:16]), 256) if nested_mask & 1 else None,
        '2': string(pointer(item[16:24]), 4096) if mask & 2 else None,
        '3': int.from_bytes(item[24:28], 'little'),
        '4': int.from_bytes(item[28:32], 'little'),
        '5': int.from_bytes(item[40:44], 'little'),
        '6': string(pointer(item[32:40]), 4096) if mask & 32 else None,
        '7': int.from_bytes(item[44:48], 'little') if mask & 64 else None,
    }
    factory_string = string(registers['x2'], 512)
    return {'item_count': 1, 'presence_mask': mask, 'nested_presence_mask': nested_mask,
            'fields': fields, 'factory_string': factory_string,
            'reads': reads, 'bytes_read': total, 'plaintext_retained': False,
            'native_called': False, 'sent_by_observer': False}
