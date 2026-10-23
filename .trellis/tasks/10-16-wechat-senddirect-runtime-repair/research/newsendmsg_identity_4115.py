"""Bounded read-only service identity snapshot; never attaches or calls native code.

0x4669774 reads singleton 0xa45df38. Constructor 0x4666b54 installs
vtable 0x9e92400. Its virtual+0x18 getter 0x466a318 reads account+0x250.
0x4668ad0 proves the aliased shared_ptr: control+0x18=owner and
control+0x28=service=owner+0x10. 0x462e4d4 installs the three vtables.
Live use still requires a new explicit single-window authorization.
"""
from __future__ import annotations

from collections.abc import Callable


def inspect_service(read: Callable[[int, int], bytes], base: int) -> dict:
    """Read at most 80 bytes; fail immediately on any unexpected identity.

    Only object/vtable/code pointers are read. No account values, keys,
    message data, memory scanning, expressions, writes or function calls.
    The supplied read must enforce its enclosing observation deadline.
    """
    if type(base) is not int or base < 4096 or base % 4096:
        raise ValueError('invalid module base')
    reads = 0

    def pointer(address: int) -> int:
        nonlocal reads
        if reads >= 12:
            raise RuntimeError('snapshot read budget exceeded')
        reads += 1
        raw = read(address, 8)
        if type(raw) is not bytes or len(raw) != 8:
            raise RuntimeError('short snapshot read')
        value = int.from_bytes(raw, 'little')
        if value < 4096 or value % 8:
            raise RuntimeError('null or unaligned object pointer')
        return value

    def exact(address: int, expected: int) -> int:
        value = pointer(address)
        if value != expected:
            raise RuntimeError('service identity mismatch')
        return value

    account = pointer(base + 0xA45DF38)
    exact(account, base + 0x9E92400)
    exact(base + 0x9E92418, base + 0x466A318)
    service = pointer(account + 0x250)
    control = pointer(account + 0x258)
    owner = service - 0x10
    if owner != control + 0x18:
        raise RuntimeError('embedded owner relationship mismatch')
    exact(control, base + 0x9E92C98)
    exact(owner, base + 0x9E8FC30)
    exact(owner + 8, base + 0x9E8FD78)
    exact(service, base + 0x9E8FDA0)
    # A code address only needs four-byte alignment, unlike the object pointers.
    raw = read(base + 0x9E8FDC8, 8)
    if type(raw) is not bytes or len(raw) != 8 or int.from_bytes(raw, 'little') != base + 0x46353A0:
        raise RuntimeError('enqueue virtual slot mismatch')
    reads += 1
    return {'account_object': hex(account), 'service_interface': hex(service),
            'owner_object': hex(owner), 'control_block': hex(control),
            'enqueue_rva': '0x46353a0', 'reads': reads, 'bytes_read': reads * 8,
            'identity_matched': True, 'native_called': False, 'sent': False}
