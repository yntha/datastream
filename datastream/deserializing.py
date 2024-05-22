import io
import struct
import typing

from enum import IntEnum


# these constants refer to the index of the byteorder character in _byteorder_map
class ByteOrder(IntEnum):
    LITTLE_ENDIAN = 0
    BIG_ENDIAN = 1
    NETWORK_ENDIAN = 2
    NATIVE_ENDIAN = 3


_byteorder_map = "!@<>"


class DeserializingStream:
    def __init__(
        self, buffer: bytes | typing.IO[bytes], byteorder: int = ByteOrder.LITTLE_ENDIAN
    ):
        if isinstance(buffer, bytes):
            self.buffer = io.BytesIO(buffer)  # internally use a BytesIO object
        else:
            self.buffer = buffer

        self._byteorder = _byteorder_map[byteorder]

    @property
    def byteorder(self) -> str:
        return ByteOrder(_byteorder_map.index(self._byteorder))

    @byteorder.setter
    def byteorder(self, value: int):
        self._byteorder = _byteorder_map[value]

    def read_format(self, fmt: str) -> typing.Any:
        return struct.unpack(
            self._byteorder + fmt, self.buffer.read(struct.calcsize(fmt))
        )[0]
    
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
