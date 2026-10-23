"""Hand-encoded wire fixtures independent of the parser's descriptor builder."""
from __future__ import annotations

import unittest

from newsendmsg_response_4115 import MAX_RESPONSE_BYTES, parse_response


def varint(value: int) -> bytes:
    result = []
    while value > 127:
        result.append((value & 127) | 128)
        value >>= 7
    return bytes([*result, value])


def blob(number: int, value: bytes) -> bytes:
    return varint(number << 3 | 2) + varint(len(value)) + value


def item(fields: tuple[int, ...] = tuple(range(1, 8)), value: int = 0,
         wrapper: bytes = b'', extra: bytes = b'') -> bytes:
    return b''.join(blob(2, wrapper) if number == 2 else
                    varint(number << 3) + varint(value)
                    for number in fields) + extra


def envelope(row: bytes | None = None, base: bytes = bytes.fromhex('08001200'),
             field_2: int = 0) -> bytes:
    return blob(1, base) + b'\x10' + varint(field_2) + (b'' if row is None else blob(3, row))


class ResponseChecks(unittest.TestCase):
    def test_hand_encoded_zero_response(self) -> None:
        wire = bytes.fromhex('0a040800120010001a0e0800120018002000280030003800')
        self.assertEqual(wire, envelope(item()))
        response = parse_response(wire)
        self.assertEqual((response.base_field_1, response.base_field_2, response.field_2), (0, None, 0))
        self.assertEqual(len(response.items), 1)
        self.assertEqual(response.items[0].field_8, None)
        self.assertFalse(response.sent)

    def test_required_presence_not_truthiness(self) -> None:
        for number in range(1, 8):
            with self.subTest(number=number), self.assertRaises(ValueError):
                parse_response(envelope(item(tuple(n for n in range(1, 8) if n != number))))
        for base in (b'', bytes.fromhex('0800'), bytes.fromhex('1200')):
            with self.subTest(base=base), self.assertRaises(ValueError):
                parse_response(envelope(base=base))
        for wire in (bytes.fromhex('0a0408001200'), bytes.fromhex('1000')):
            with self.assertRaises(ValueError):
                parse_response(wire)

    def test_empty_list_and_independent_field_2_are_preserved(self) -> None:
        result = parse_response(envelope(field_2=999))
        self.assertEqual(result.items, ())
        self.assertEqual(result.field_2, 999)
        self.assertFalse(result.sent)

    def test_optional_wrapper_bytes_absent_and_empty_differ(self) -> None:
        absent = parse_response(envelope(item()))
        present = parse_response(envelope(item(wrapper=b'\x0a\x00'), base=bytes.fromhex('080012020a00')))
        self.assertIsNone(absent.base_field_2)
        self.assertIsNone(absent.items[0].field_2)
        self.assertEqual(present.base_field_2, b'')
        self.assertEqual(present.items[0].field_2, b'')

    def test_signed_error_and_wide_numbers(self) -> None:
        signed = b'\x08' + varint((1 << 64) - 13)
        row = signed + item(tuple(range(2, 8)), value=(1 << 32) - 1,
                            wrapper=blob(1, '合成回执'.encode()),
                            extra=b'\x40' + varint((1 << 64) - 1))
        result = parse_response(envelope(row, base=signed + b'\x12\x00'))
        self.assertEqual(result.base_field_1, -13)
        self.assertEqual(result.items[0].field_1, -13)
        self.assertEqual(result.items[0].field_7, (1 << 32) - 1)
        self.assertEqual(result.items[0].field_8, (1 << 64) - 1)
        self.assertEqual(result.items[0].field_2, '合成回执'.encode())
        self.assertFalse(result.sent)

    def test_unknown_fields_and_duplicate_scalar_use_proto_semantics(self) -> None:
        wire = envelope(item(extra=b'\x40\x00\x40\x01')) + blob(100, b'extension')
        self.assertEqual(parse_response(wire).items[0].field_8, 1)

    def test_malformed_nested_and_wrong_wire_types(self) -> None:
        for wire in (envelope() + b'\x1a\x80', envelope(b'\x00'), envelope(b'\x12\x02\x0a'),
                     bytes.fromhex('0a04080012001500000000')):
            with self.subTest(wire=wire), self.assertRaises(ValueError):
                parse_response(wire)

    def test_allocation_and_type_bounds(self) -> None:
        for value in (b'', b'x' * (MAX_RESPONSE_BYTES + 1)):
            with self.assertRaises(ValueError):
                parse_response(value)
        for value in (bytearray(envelope()), memoryview(envelope()), 'text'):
            with self.assertRaises(TypeError):
                parse_response(value)
        with self.assertRaises(ValueError):
            parse_response(envelope() + blob(3, item()) * 1025)


if __name__ == '__main__':
    unittest.main(verbosity=2)
