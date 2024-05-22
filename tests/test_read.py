import io

from datastream import DeserializingStream


def test_stream_read():
    iostream = io.BytesIO()

    iostream.write(bytes.fromhex("FF FF FF FF"))
    iostream.write(bytes.fromhex("FF FF FF FF"))
    iostream.write(bytes.fromhex("FF FF"))
    iostream.write(bytes.fromhex("FF"))

    iostream.seek(0)

    # ensure that the DeserializingStream class accepts buffers and streams alike
    stream = DeserializingStream(iostream)
    stream = DeserializingStream(iostream.getvalue())

    assert stream.read_int32() == -1
    assert stream.read_uint32() == 0xFFFFFFFF
    assert stream.read_int16() == -1
    assert stream.read_uint8() == 0xFF

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
