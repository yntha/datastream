import io
import typing
from enum import IntEnum


# these constants refer to the index of the byteorder character in _byteorder_map
class ByteOrder(IntEnum):
    """
    Enumeration representing byte order options.

    Attributes:
        LITTLE_ENDIAN (int): Represents little-endian byte order.
        BIG_ENDIAN (int): Represents big-endian byte order.
        NETWORK_ENDIAN (int): Represents network byte order.
        NATIVE_ENDIAN (int): Represents native byte order.
    """
    LITTLE_ENDIAN = 0
    BIG_ENDIAN = 1
    NETWORK_ENDIAN = 2
    NATIVE_ENDIAN = 3


_byteorder_map = "!@<>"


class BaseStream:
    def __init__(self, backing_stream: typing.IO[bytes], byteorder: int):
        if not isinstance(backing_stream, io.BytesIO):
            raise ValueError("backing_stream must be a BytesIO object")

        self._backing_stream = backing_stream
        self._byteorder = _byteorder_map[byteorder]

    @property
    def byteorder(self) -> str:
        return ByteOrder(_byteorder_map.index(self._byteorder))

    @byteorder.setter
    def byteorder(self, value: int):
        self._byteorder = _byteorder_map[value]

    def read(self, size: int) -> bytes:
        return self._backing_stream.read(size)

    def size(self) -> int:
        return len(self._backing_stream.getvalue())

    def remaining(self) -> int:
        return self.size() - self.tell()

    def seek(self, offset: int, whence: int = io.SEEK_SET):
        self._backing_stream.seek(offset, whence)

    def tell(self) -> int:
        return self._backing_stream.tell()

    def close(self):
        self._backing_stream.close()

    def write(self, data: bytes):
        self._backing_stream.write(data)

    def clone(self) -> typing.Self:
        return self.__class__(
            io.BytesIO(self._backing_stream.getvalue()), self.byteorder
        )

    def substream(self, start: int, end: int) -> typing.Self:
        return self.__class__(
            io.BytesIO(self._backing_stream.getvalue()[start:end]), self.byteorder
        )

    def peek(self, size: int) -> bytes:
        pos = self.tell()
        data = self.read(size)

        self.seek(pos)

        return data

    def seekpeek(self, offset: int, size: int) -> bytes:
        pos = self.tell()
        self.seek(offset)

        data = self.read(size)
        self.seek(pos)

        return data

    def search(self, data: bytes) -> int:
        pos = self.tell()

        while True:
            chunk = self.read(len(data))
            if not chunk:
                self.seek(pos)

                return -1
            if chunk == data:
                index = self.tell() - len(data)
                self.seek(pos)

                return index

            self.seek(self.tell() - len(data) + 1)

    def clear(self):
        self._backing_stream.truncate(0)
        self._backing_stream.seek(0)
