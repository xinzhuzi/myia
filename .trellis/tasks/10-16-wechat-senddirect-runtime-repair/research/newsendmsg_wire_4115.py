"""Offline numbered newsendmsg wire fields for frozen WeChat 4.1.15.

Sources: body serializer 0x465da58, item 0x465d024/init 0x465d30c,
wrapper 0x4f37c94/parser 0x4f37b88/init 0x4f37d40.
No I/O, native calls, Task construction, account packaging, or sending.
Ordinals are deliberate: original business field names are not established.
"""
from __future__ import annotations

from dataclasses import dataclass

MAX_BODY_BYTES = 16 * 1024 * 1024  # Local research bound, not a native limit.
MAX_ITEMS = 1024


@dataclass(frozen=True)
class MessageItem:
    """Explicit native field values; None means absent for optional fields.

    field_1 is the optional bytes inside the required nested wrapper.
    Callers supply field_5 explicitly; this module does not synthesize its
    source from a clock or infer the native helper's business semantics.
    """

    field_1: bytes | None
    field_3: int
    field_4: int
    field_5: int
    field_2: bytes | None = None
    field_6: bytes | None = None
    field_7: int | None = None


def _varint(value: int) -> bytes:
    result = bytearray()
    while value >= 128:
        result.append((value & 127) | 128)
        value >>= 7
    result.append(value)
    return bytes(result)


def _uint32(number: int, value: int) -> bytes:
    if type(value) is not int or not 0 <= value <= 0xFFFFFFFF:
        raise ValueError(f'field_{number} must be uint32')
    return _varint(number << 3) + _varint(value)


def _bytes(number: int, value: bytes) -> bytes:
    if type(value) is not bytes:
        raise TypeError(f'field_{number} must be immutable bytes')
    if len(value) > MAX_BODY_BYTES:
        raise ValueError('field exceeds the local allocation bound')
    return _varint((number << 3) | 2) + _varint(len(value)) + value


def _item(item: MessageItem) -> bytes:
    if type(item) is not MessageItem:
        raise TypeError('items must contain MessageItem instances')
    wrapper = b'' if item.field_1 is None else _bytes(1, item.field_1)
    parts = [_bytes(1, wrapper)]
    if item.field_2 is not None:
        parts.append(_bytes(2, item.field_2))
    parts.extend((_uint32(3, item.field_3), _uint32(4, item.field_4), _uint32(5, item.field_5)))
    if item.field_6 is not None:
        parts.append(_bytes(6, item.field_6))
    if item.field_7 is not None:
        parts.append(_uint32(7, item.field_7))
    if sum(map(len, parts)) > MAX_BODY_BYTES:
        raise ValueError('item exceeds the local allocation bound')
    return b''.join(parts)


def build_request(items: tuple[MessageItem, ...]) -> bytes:
    """Encode item count and ordered items, preserving required zero values.

    Native IsInitialized only requires count presence and valid items; the
    local API additionally enforces 1..1024 items and count=len(items).
    Output is the inner request only. It is not Task+0x1c8 or final x4 data.
    """
    if type(items) is not tuple:
        raise TypeError('items must be an immutable tuple')
    if not 1 <= len(items) <= MAX_ITEMS:
        raise ValueError('items must contain 1..1024 entries')
    result = bytearray(_uint32(1, len(items)))
    for item in items:
        encoded = _bytes(2, _item(item))
        if len(result) + len(encoded) > MAX_BODY_BYTES:
            raise ValueError('request exceeds the local allocation bound')
        result.extend(encoded)
    return bytes(result)
