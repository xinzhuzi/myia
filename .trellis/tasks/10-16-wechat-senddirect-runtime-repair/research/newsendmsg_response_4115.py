"""Offline parser for copied 4.1.15 response wire; no delivery claim or I/O.

Field ordinals/types come from native parsers 0x465ef20/0x465e144/0x465b43c.
Required masks: outer3 (0x465f4a0), base3 (0x465b7a0), item0x7f
(0x465e934). Business names and request/response correlation are not inferred.
Research dependency: google.protobuf, already used by the independent wire oracle.
"""
from __future__ import annotations

from dataclasses import dataclass

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from google.protobuf.message import DecodeError

MAX_RESPONSE_BYTES = 16 * 1024 * 1024
MAX_RESPONSE_ITEMS = 1024


def _response_class():
    schema = descriptor_pb2.FileDescriptorProto(name='newsendmsg_response_4115.proto', syntax='proto2')
    wrapper = schema.message_type.add(name='Wrapper')
    wrapper.field.add(name='field_1', number=1, type=12, label=1)
    base = schema.message_type.add(name='Base')
    base.field.add(name='field_1', number=1, type=5, label=2)
    base.field.add(name='field_2', number=2, type=11, label=2, type_name='.Wrapper')
    item = schema.message_type.add(name='Item')
    item.field.add(name='field_1', number=1, type=5, label=2)
    item.field.add(name='field_2', number=2, type=11, label=2, type_name='.Wrapper')
    for number in range(3, 8):
        item.field.add(name=f'field_{number}', number=number, type=13, label=2)
    item.field.add(name='field_8', number=8, type=4, label=1)
    response = schema.message_type.add(name='Response')
    response.field.add(name='field_1', number=1, type=11, label=2, type_name='.Base')
    response.field.add(name='field_2', number=2, type=13, label=2)
    response.field.add(name='field_3', number=3, type=11, label=3, type_name='.Item')
    pool = descriptor_pool.DescriptorPool()
    pool.Add(schema)
    return message_factory.GetMessageClass(pool.FindMessageTypeByName('Response'))


_Response = _response_class()


@dataclass(frozen=True)
class ResponseItem:
    field_1: int
    field_2: bytes | None
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int | None


@dataclass(frozen=True)
class ParsedResponse:
    base_field_1: int
    base_field_2: bytes | None
    field_2: int
    items: tuple[ResponseItem, ...]
    sent: bool = False  # Parsing is never an independent delivery observation.


def parse_response(data: bytes) -> ParsedResponse:
    """Parse native copied wire, enforcing required presence and local bounds.

    The native required masks permit empty lists and empty wrappers; preserve
    these states. Do not assign semantics to field_2 or equate it to list size.
    Unknown fields are accepted by protobuf and ignored by this result view.
    """
    if type(data) is not bytes:
        raise TypeError('response must be immutable bytes')
    if not data or len(data) > MAX_RESPONSE_BYTES:
        raise ValueError('response violates local allocation bound')
    response = _Response()
    try:
        response.ParseFromString(data)
    except DecodeError as error:
        raise ValueError('malformed native response wire') from error
    if not response.IsInitialized():
        raise ValueError('native response is missing required fields')
    if len(response.field_3) > MAX_RESPONSE_ITEMS:
        raise ValueError('response violates local item bound')
    base = response.field_1
    return ParsedResponse(
        base.field_1,
        base.field_2.field_1 if base.field_2.HasField('field_1') else None,
        response.field_2,
        tuple(ResponseItem(
            item.field_1,
            item.field_2.field_1 if item.field_2.HasField('field_1') else None,
            item.field_3, item.field_4, item.field_5, item.field_6, item.field_7,
            item.field_8 if item.HasField('field_8') else None,
        ) for item in response.field_3),
    )
