import io
import struct

import pytest
from datastream import ByteOrder, SerializingStream, TwoWayStream


def test_serializer_constructor():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    assert stream.byteorder == ByteOrder.NATIVE_ENDIAN
    assert bytes(stream) == b""

    stream = SerializingStream(byteorder=ByteOrder.LITTLE_ENDIAN)

    assert stream.byteorder == ByteOrder.LITTLE_ENDIAN
    assert bytes(stream) == b""


def test_twoway_stream_write():
    stream = TwoWayStream()

    stream.write_uint32(0xFFFFFFFF)

    assert bytes(stream) == bytes.fromhex("FF FF FF FF")


def test_serializer_write_format():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_format("q", -1)

    assert bytes(stream) == bytes.fromhex("FF FF FF FF FF FF FF FF")


def test_serializer_write_format_invalid():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    with pytest.raises(struct.error):
        stream.write_format("z", 0)

    with pytest.raises(struct.error):
        stream.write_format("b", 0xFFFF)


def test_serializer_write_int64():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_int64(-1)

    assert bytes(stream) == bytes.fromhex("FF FF FF FF FF FF FF FF")


def test_serializer_write_uint64():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_uint64(0xFFFFFFFFFFFFFFFF)

    assert bytes(stream) == bytes.fromhex("FF FF FF FF FF FF FF FF")


def test_serializer_write_int32():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_int32(-1)

    assert bytes(stream) == bytes.fromhex("FF FF FF FF")


def test_serializer_write_uint32():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_uint32(0xFFFFFFFF)

    assert bytes(stream) == bytes.fromhex("FF FF FF FF")


def test_serializer_write_int16():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_int16(-1)

    assert bytes(stream) == bytes.fromhex("FF FF")


def test_serializer_write_uint16():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_uint16(0xFFFF)

    assert bytes(stream) == bytes.fromhex("FF FF")


def test_serializer_write_int8():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_int8(-1)

    assert bytes(stream) == bytes.fromhex("FF")


def test_serializer_write_uint8():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_uint8(0xFF)

    assert bytes(stream) == bytes.fromhex("FF")


def test_serializer_write_float():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream, ByteOrder.BIG_ENDIAN)

    stream.write_float(1.0)

    assert bytes(stream) == bytes.fromhex("00 00 80 3F")


def test_serializer_write_double():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream, ByteOrder.BIG_ENDIAN)

    stream.write_double(1.0)

    assert bytes(stream) == bytes.fromhex("00 00 00 00 00 00 F0 3F")


def test_serializer_write_bool():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write_bool(True)

    assert bytes(stream) == bytes.fromhex("01")

    stream.clear()
    stream.write_bool(False)

    assert bytes(stream) == bytes.fromhex("00")


def test_serializer_write_bytes():
    iostream = io.BytesIO()
    stream = SerializingStream(iostream)

    stream.write(b"\x00\x01\x02\x03")

    assert bytes(stream) == bytes.fromhex("00 01 02 03")
