"""Synthetic proto2 oracle for the independently retained native wire contract."""
from __future__ import annotations

import unittest

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

from newsendmsg_wire_4115 import MAX_BODY_BYTES, MessageItem, build_request

schema = descriptor_pb2.FileDescriptorProto(name='newsendmsg_4115.proto', syntax='proto2')
wrapper = schema.message_type.add(name='StringWrapper')
wrapper.field.add(name='field_1', number=1, type=12, label=1)
item = schema.message_type.add(name='Item')
for number, kind, label, nested in (
    (1, 11, 2, '.StringWrapper'), (2, 12, 1, ''),
    (3, 13, 2, ''), (4, 13, 2, ''), (5, 13, 2, ''),
    (6, 12, 1, ''), (7, 13, 1, ''),
):
    field = item.field.add(name=f'field_{number}', number=number, type=kind, label=label)
    if nested:
        field.type_name = nested
request = schema.message_type.add(name='Request')
request.field.add(name='field_1', number=1, type=13, label=2)
request.field.add(name='field_2', number=2, type=11, label=3, type_name='.Item')
pool = descriptor_pool.DescriptorPool()
pool.Add(schema)
Request = message_factory.GetMessageClass(pool.FindMessageTypeByName('Request'))


class NewsendmsgWireChecks(unittest.TestCase):
    def test_independent_protobuf_serialization(self) -> None:
        for size in (0, 1, 127, 128, 16383, 16384):
            for value in (0, 127, 128, 0xFFFFFFFF):
                with self.subTest(size=size, value=value):
                    source = MessageItem('合成对象'.encode(), value, value, value,
                                         field_2=b'x' * size, field_6=b'', field_7=0)
                    expected = Request(field_1=1)
                    row = expected.field_2.add(field_2=b'x' * size, field_3=value,
                                               field_4=value, field_5=value, field_6=b'', field_7=0)
                    row.field_1.field_1 = '合成对象'.encode()
                    self.assertEqual(build_request((source,)), expected.SerializeToString(deterministic=True))

    def test_explicit_required_zero_values(self) -> None:
        data = build_request((MessageItem(b'', 0, 0, 0),))
        self.assertEqual(data, bytes.fromhex('0801120a0a020a00180020002800'))
        decoded = Request.FromString(data)
        self.assertTrue(decoded.IsInitialized())
        for number in (3, 4, 5):
            self.assertTrue(decoded.field_2[0].HasField(f'field_{number}'))

    def test_optional_wrapper_string_can_be_absent(self) -> None:
        decoded = Request.FromString(build_request((MessageItem(None, 1, 2, 3),)))
        self.assertTrue(decoded.IsInitialized())
        self.assertTrue(decoded.field_2[0].HasField('field_1'))
        self.assertFalse(decoded.field_2[0].field_1.HasField('field_1'))

    def test_each_required_item_field_is_needed(self) -> None:
        for name in ('field_1', 'field_3', 'field_4', 'field_5'):
            row = Request.FromString(build_request((MessageItem(b'x', 1, 2, 3),)))
            row.field_2[0].ClearField(name)
            self.assertFalse(row.IsInitialized(), name)

    def test_repeated_items_preserve_order_and_count(self) -> None:
        decoded = Request.FromString(build_request(tuple(MessageItem(b'x', n, 0, 0) for n in range(3))))
        self.assertEqual(decoded.field_1, 3)
        self.assertEqual([row.field_3 for row in decoded.field_2], [0, 1, 2])

    def test_optional_absent_differs_from_present_empty_and_zero(self) -> None:
        absent = Request.FromString(build_request((MessageItem(b'x', 1, 2, 3),)))
        present = Request.FromString(build_request((MessageItem(b'x', 1, 2, 3, b'', b'', 0),)))
        for number in (2, 6, 7):
            self.assertFalse(absent.field_2[0].HasField(f'field_{number}'))
            self.assertTrue(present.field_2[0].HasField(f'field_{number}'))

    def test_invalid_values_fail_before_serialization(self) -> None:
        for value in (-1, 1 << 32, True, '1', 1.5):
            for name in ('field_3', 'field_4', 'field_5', 'field_7'):
                args = dict(field_1=b'x', field_3=0, field_4=0, field_5=0)
                args[name] = value
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    build_request((MessageItem(**args),))
        for name in ('field_1', 'field_2', 'field_6'):
            for value in ('text', bytearray(b'x'), memoryview(b'x')):
                args = dict(field_1=b'x', field_3=0, field_4=0, field_5=0)
                args[name] = value
                with self.subTest(name=name), self.assertRaises(TypeError):
                    build_request((MessageItem(**args),))

    def test_local_allocation_limits(self) -> None:
        for items in ((), tuple(MessageItem(b'', 0, 0, 0) for _ in range(1025))):
            with self.assertRaises(ValueError):
                build_request(items)
        with self.assertRaises(ValueError):
            build_request((MessageItem(b'x', 0, 0, 0, b'x' * MAX_BODY_BYTES),))
        with self.assertRaises(TypeError):
            build_request([MessageItem(b'x', 0, 0, 0)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
