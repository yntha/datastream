import io
import struct
import typing

from datastream.base import BaseStream, ByteOrder


class DeserializingStream(BaseStream):
    def __init__(
        self, buffer: bytes | typing.IO[bytes], byteorder: int = ByteOrder.LITTLE_ENDIAN
    ):
        if not isinstance(buffer, io.BytesIO):
            if isinstance(buffer, io.BaseIO):
                buffer = io.BytesIO(buffer.getvalue())
            else:
                buffer = io.BytesIO(buffer)

        super().__init__(buffer, byteorder)

    def read_format(self, fmt: str) -> typing.Any:
        return struct.unpack(self._byteorder + fmt, self.read(struct.calcsize(fmt)))[0]

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
