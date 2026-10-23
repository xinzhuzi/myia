"""Offline base MMReq envelope, derived from the verified 4.1.15 producer.

This covers the base fields written by 0x4634710, using wire tags from
0x55653ac and required-field checks from 0x55657b0/0x5ce61ec.
It does not resolve account-dependent extensions, construct a Task, invoke
native code, attach a debugger, or send anything. It is not a send adapter.
Native field names are unavailable; field_1 deliberately retains its ordinal.
"""
from __future__ import annotations

MAX_REQUEST_BYTES = 16 * 1024 * 1024  # Local research allocation bound.


def _uint64(value: int) -> bytes:
    """Encode an already validated unsigned integer without lossy conversion."""
    encoded = bytearray()
    while value >= 0x80:
        encoded.append((value & 0x7F) | 0x80)
        value >>= 7
    encoded.append(value)
    return bytes(encoded)


def build_base_mmreq(field_1: int, request_body: bytes) -> bytes:
    """Wrap opaque request bytes in the proven base envelope, without I/O.

    Field 1 is the value obtained through the account object's vtable+0x20
    in the native producer; its original name is not established here.
    The native required-field mask is 0xf: fields 1, 2, 3 and 4 must be
    present even when their value is zero/false. The producer also emits
    optional field 5=false. Optional fields 7/9/10/11 remain outside this
    base implementation and must not be silently ignored in a send driver.
    """
    if type(field_1) is not int or not 0 <= field_1 <= 0xFFFFFFFFFFFFFFFF:
        raise ValueError('field_1 must be an unsigned 64-bit integer')
    if not isinstance(request_body, bytes):
        raise TypeError('request_body must be immutable bytes')
    if not request_body or len(request_body) > MAX_REQUEST_BYTES:
        raise ValueError('request_body must contain 1..16777216 bytes')
    return b''.join((
        b'\x08', _uint64(field_1),
        b'\x12', _uint64(len(request_body)), request_body,
        b'\x18\x00',  # Field 3: int32, explicitly present zero.
        b'\x20\x00',  # Field 4: bool, explicitly present false (required).
        b'\x28\x00',  # Field 5: bool, explicitly present false (optional).
    ))
