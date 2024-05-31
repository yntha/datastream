import io
import typing

from datastream.base import BaseStream, ByteOrder
from datastream.deserializing import DeserializingStream
from datastream.serializing import SerializingStream


class TwoWayStream(BaseStream):
    def __init__(
        self,
        buffer: bytes | typing.IO[bytes] | None = None,
        byteorder: int = ByteOrder.NATIVE_ENDIAN,
    ):
        if buffer is None:
            buffer = io.BytesIO()
        elif isinstance(buffer, bytes):
            buffer = io.BytesIO(buffer)

        self.dstream = DeserializingStream(buffer, byteorder)
        self.sstream = SerializingStream(buffer, byteorder) # type: ignore

        super().__init__(buffer, byteorder) # type: ignore

    def read_format(self, fmt: str) -> typing.Any:
        return self.dstream.read_format(fmt)

    def read_int64(self) -> int:
        return self.read_format("q")

    def read_uint64(self) -> int:
        return self.read_format("Q")

    def read_int32(self) -> int:
        return self.read_format("i")

    def read_uint32(self) -> int:
        return self.read_format("I")

    def read_int16(self) -> int:
        return self.read_format("h")

    def read_uint16(self) -> int:
        return self.read_format("H")

    def read_int8(self) -> int:
        return self.read_format("b")

    def read_uint8(self) -> int:
        return self.read_format("B")

    def read_float(self) -> float:
        return self.read_format("f")

    def read_double(self) -> float:
        return self.read_format("d")

    def read_bool(self) -> bool:
        return bool(self.read_uint8())

    def read_uleb128(self) -> int:
        return self.read_uleb128_safe(-1)

    def read_uleb128_safe(self, max_bytes: int = 16) -> int:
        return self.dstream.read_uleb128_safe(max_bytes)

    def read_sleb128(self) -> int:
        return self.read_sleb128_safe(-1)

    def read_sleb128_safe(self, stop_after: int = 5) -> int:
        return self.dstream.read_sleb128_safe(stop_after)

    def bytes(self) -> bytes:
        return self.sstream.bytes()

    def __bytes__(self) -> bytes: # type: ignore
        return self.bytes()

    def write_format(self, fmt: str, value: typing.Any):
        self.sstream.write_format(fmt, value)

    def write_int64(self, value: int):
        self.write_format("q", value)

    def write_uint64(self, value: int):
        self.write_format("Q", value)

    def write_int32(self, value: int):
        self.write_format("i", value)

    def write_uint32(self, value: int):
        self.write_format("I", value)

    def write_int16(self, value: int):
        self.write_format("h", value)

    def write_uint16(self, value: int):
        self.write_format("H", value)

    def write_int8(self, value: int):
        self.write_format("b", value)

    def write_uint8(self, value: int):
        self.write_format("B", value)

    def write_float(self, value: float):
        self.write_format("f", value)

    def write_double(self, value: float):
        self.write_format("d", value)

    def write_bool(self, value: bool):
        self.write_uint8(int(value))

    def write_uleb128(self, value: int):
        self.write_uleb128_safe(value, -1)

    def write_uleb128_safe(self, value: int, max_bytes: int = 16):
        self.sstream.write_uleb128_safe(value, max_bytes)

    def write_sleb128(self, value: int):
        return self.write_sleb128_safe(value, -1)

    def write_sleb128_safe(self, value: int, max_bytes: int = 5):
        self.sstream.write_sleb128_safe(value, max_bytes)
