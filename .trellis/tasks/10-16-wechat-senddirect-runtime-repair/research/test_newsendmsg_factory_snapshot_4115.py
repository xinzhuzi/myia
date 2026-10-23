"""Synthetic layout and privacy checks independent of any live process."""
from __future__ import annotations

import hashlib
import struct

import pytest

from newsendmsg_factory_snapshot_4115 import inspect_factory

BASE = 0x100000000
SERVICE = 0x200000000
BODY, ITEMS, ITEM, WRAPPER = 0x300000000, 0x300000100, 0x300000200, 0x300000300
DEST, CONTENT, SOURCE, FACTORY, PAYLOAD = (0x300000400, 0x300000500, 0x300000600,
                                          0x300000700, 0x300000800)


def graph(content=b'a' * 64, mask=0x3F):
    memory = {}

    def put(address, raw):
        memory.update({address + index: byte for index, byte in enumerate(raw)})

    def short(value):
        assert len(value) <= 22
        return value + bytes(23 - len(value)) + bytes([len(value)])

    put(BODY, struct.pack('<QQiiiIIIQ', BASE + 0x9E91DF8, ITEMS, 1, 1, 1, 0, 1, 0, 1))
    put(ITEMS, struct.pack('<Q', ITEM))
    put(ITEM, struct.pack('<QQQIIQIIII', BASE + 0x9E91D80, WRAPPER, CONTENT,
                          1, 1700000000, SOURCE, 12345, 77, 0, mask))
    put(WRAPPER, struct.pack('<QQII', BASE + 0x9ECA390, DEST, 0, 1))
    put(DEST, short(b'filehelper'))
    if len(content) <= 22:
        put(CONTENT, short(content))
    else:
        put(CONTENT, struct.pack('<QQQ', PAYLOAD, len(content), (len(content) + 1) | (1 << 63)))
        put(PAYLOAD, content)
    put(SOURCE, short(b'source'))
    put(FACTORY, short(b'factory'))

    def read(address, length):
        return bytes(memory[address + index] for index in range(length))

    registers = {'x0': SERVICE, 'x1': BODY, 'x2': FACTORY}
    return memory, put, read, registers


def test_snapshot_numbered_values_and_privacy():
    _, _, read, registers = graph()
    result = inspect_factory(read, BASE, registers, SERVICE)
    assert result['fields']['3'] == 1
    assert result['fields']['4'] == 1700000000
    assert result['fields']['5'] == 12345
    assert result['fields']['7'] is None
    assert result['fields']['1'] == {'bytes': 10, 'sha256': hashlib.sha256(b'filehelper').hexdigest()}
    assert result['fields']['2']['sha256'] == hashlib.sha256(b'a' * 64).hexdigest()
    assert 'filehelper' not in str(result) and 'factory' not in str(result['factory_string'])
    assert result['bytes_read'] < 12288 and not result['plaintext_retained']
    assert not result['native_called'] and not result['sent_by_observer']


@pytest.mark.parametrize('content', [b'', b'abc', b'x' * 22, b'x' * 23, b'x' * 4096])
def test_short_long_and_empty(content):
    _, _, read, registers = graph(content)
    assert inspect_factory(read, BASE, registers, SERVICE)['fields']['2'] == {
        'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()}


def test_optional_absent_does_not_read_pointer():
    _, _, read, registers = graph(mask=0x1D)
    fields = inspect_factory(read, BASE, registers, SERVICE)['fields']
    assert fields['2'] is None and fields['6'] is None


@pytest.mark.parametrize('address,raw', [
    (BODY, struct.pack('<Q', 0)), (BODY + 16, struct.pack('<i', 2)),
    (BODY + 20, struct.pack('<i', 0)), (BODY + 24, struct.pack('<i', 1025)),
    (BODY + 32, struct.pack('<I', 0)), (BODY + 40, struct.pack('<I', 0)),
    (ITEMS, struct.pack('<Q', 0)), (ITEM, struct.pack('<Q', 0)),
    (ITEM + 52, struct.pack('<I', 0)), (WRAPPER, struct.pack('<Q', 0)),
    (CONTENT + 8, struct.pack('<Q', 4097)),
    (CONTENT + 16, struct.pack('<Q', 64 | (1 << 63))),
    (CONTENT, struct.pack('<Q', PAYLOAD + 1)),
])
def test_corrupt_layout_rejected(address, raw):
    _, put, read, registers = graph()
    put(address, raw)
    with pytest.raises(ValueError):
        inspect_factory(read, BASE, registers, SERVICE)


def test_short_read_and_wrong_service_rejected():
    _, _, read, registers = graph()
    with pytest.raises(ValueError, match='short snapshot'):
        inspect_factory(lambda address, size: read(address, size)[:-1], BASE, registers, SERVICE)
    with pytest.raises(ValueError, match='service'):
        inspect_factory(read, BASE, registers, SERVICE + 8)


def test_reader_cancellation_propagates():
    _, _, _, registers = graph()

    def cancelled(_address, _length):
        raise InterruptedError('cancelled')

    with pytest.raises(InterruptedError):
        inspect_factory(cancelled, BASE, registers, SERVICE)
