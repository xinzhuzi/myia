"""Independent protobuf-runtime checks; entirely synthetic and offline."""
from __future__ import annotations

import unittest

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

from mmreq_base_4115 import MAX_REQUEST_BYTES, build_base_mmreq

schema = descriptor_pb2.FileDescriptorProto(name='offline_mmreq_4115.proto', syntax='proto2')
message = schema.message_type.add(name='ObservedBaseEnvelope')
# Ordinals, types and presence are independently transcribed from producer
# 0x55653ac, consumer 0x5ce5654 and required-field check 0x5ce61ec.
for ordinal, kind, label in (
    (1, descriptor_pb2.FieldDescriptorProto.TYPE_UINT64, 2),
    (2, descriptor_pb2.FieldDescriptorProto.TYPE_BYTES, 2),
    (3, descriptor_pb2.FieldDescriptorProto.TYPE_INT32, 2),
    (4, descriptor_pb2.FieldDescriptorProto.TYPE_BOOL, 2),
    (5, descriptor_pb2.FieldDescriptorProto.TYPE_BOOL, 1),
):
    message.field.add(name=f'field_{ordinal}', number=ordinal, type=kind, label=label)
pool = descriptor_pool.DescriptorPool()
pool.Add(schema)
Envelope = message_factory.GetMessageClass(pool.FindMessageTypeByName('ObservedBaseEnvelope'))


class BaseEnvelopeChecks(unittest.TestCase):
    def test_independent_runtime_and_presence(self) -> None:
        for field_1 in (0, 127, 128, 0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF):
            for body in ('离线核验'.encode(), b'\x00\xff', b'x' * 127, b'x' * 128, b'x' * 1000):
                with self.subTest(field_1=field_1, length=len(body)):
                    encoded = build_base_mmreq(field_1, body)
                    decoded = Envelope.FromString(encoded)
                    self.assertTrue(decoded.IsInitialized())
                    self.assertEqual(decoded.field_1, field_1)
                    self.assertEqual(decoded.field_2, body)
                    self.assertEqual([field.number for field, _ in decoded.ListFields()], [1, 2, 3, 4, 5])
                    independent = Envelope(field_1=field_1, field_2=body, field_3=0, field_4=False, field_5=False)
                    self.assertEqual(encoded, independent.SerializeToString(deterministic=True))

    def test_raw_body_is_not_the_envelope(self) -> None:
        raw_body = b'\x08\x01\x12\x06abcdef'
        self.assertFalse(Envelope.FromString(raw_body).IsInitialized())
        wrapped = Envelope.FromString(build_base_mmreq(1, raw_body))
        self.assertTrue(wrapped.IsInitialized())
        self.assertEqual(wrapped.field_2, raw_body)

    def test_omitting_required_false_breaks_initialization(self) -> None:
        raw = build_base_mmreq(1, b'x')
        # Remove only the independently located field-4 encoding, preserving field 5.
        self.assertEqual(raw[-4:], b'\x20\x00\x28\x00')
        incomplete = Envelope.FromString(raw[:-4] + raw[-2:])
        self.assertFalse(incomplete.IsInitialized())
        self.assertEqual(incomplete.FindInitializationErrors(), ['field_4'])

    def test_invalid_account_values_rejected(self) -> None:
        for value in (-1, 1 << 64, True, '1', 1.5, None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_base_mmreq(value, b'x')

    def test_body_type_and_allocation_bound(self) -> None:
        for body in ('x', bytearray(b'x'), memoryview(b'x'), None):
            with self.subTest(kind=type(body)), self.assertRaises(TypeError):
                build_base_mmreq(1, body)
        for body in (b'', b'x' * (MAX_REQUEST_BYTES + 1)):
            with self.subTest(length=len(body)), self.assertRaises(ValueError):
                build_base_mmreq(1, body)


if __name__ == '__main__':
    unittest.main(verbosity=2)
