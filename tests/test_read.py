import io
import struct

import pytest
from datastream import DeserializingStream, TwoWayStream


def test_stream_read():
    iostream = io.BytesIO()

    iostream.write(bytes.fromhex("FF FF FF FF"))

    iostream.seek(0)

    # ensure that the DeserializingStream class accepts buffers and streams alike
    stream = DeserializingStream(iostream)
    stream = DeserializingStream(iostream.getvalue())  # noqa: F841


def test_twoway_stream_read():
    iostream = io.BytesIO()

    iostream.write(bytes.fromhex("FF FF FF FF"))

    iostream.seek(0)

    stream = TwoWayStream(iostream)

    assert stream.read_uint32() == 0xFFFFFFFF


def test_stream_read_format():
    iostream = io.BytesIO()

    iostream.write(bytes.fromhex("FF FF FF FF"))
    iostream.write(bytes.fromhex("FF FF FF FF"))
    iostream.write(bytes.fromhex("FF FF"))
    iostream.write(bytes.fromhex("FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_format("i") == -1
    assert stream.read_format("I") == 0xFFFFFFFF
    assert stream.read_format("h") == -1
    assert stream.read_format("B") == 0xFF


def test_stream_read_invalid_format():
    iostream = io.BytesIO()

    iostream.write(bytes.fromhex("FF FF FF FF"))
    iostream.write(bytes.fromhex("FF FF FF FF"))
    iostream.write(bytes.fromhex("FF FF"))
    iostream.write(bytes.fromhex("FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    with pytest.raises(struct.error):
        stream.read_format("z")

    with pytest.raises(struct.error):
        stream.read_format("qq")


def test_stream_read_until():
    iostream = io.BytesIO()

    iostream.write(bytes.fromhex("DEADBEEF00"))
    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_until(b"\x00") == b"\xDE\xAD\xBE\xEF\x00"


def test_stream_read_int64():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF FF FF FF FF FF FF FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_int64() == -1


def test_stream_read_uint64():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF FF FF FF FF FF FF FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_uint64() == 0xFFFFFFFFFFFFFFFF


def test_stream_read_int32():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF FF FF FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_int32() == -1


def test_stream_read_uint32():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF FF FF FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_uint32() == 0xFFFFFFFF


def test_stream_read_int16():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_int16() == -1


def test_stream_read_uint16():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_uint16() == 0xFFFF


def test_stream_read_int8():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_int8() == -1


def test_stream_read_uint8():
    iostream = io.BytesIO()
    iostream.write(bytes.fromhex("FF"))

    iostream.seek(0)

    stream = DeserializingStream(iostream)

    assert stream.read_uint8() == 0xFF
