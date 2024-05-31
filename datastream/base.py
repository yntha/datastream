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
    """
    Base class for stream operations.

    Args:
        backing_stream (typing.IO[bytes]): The backing stream object.
        byteorder (int): The byte order of the stream.
    """

    def __init__(self, backing_stream: typing.IO[bytes], byteorder: int):
        if backing_stream is None:
            return
        
        if not isinstance(backing_stream, io.BytesIO):
            raise ValueError("backing_stream must be a BytesIO object")

        self._backing_stream = backing_stream
        self._byteorder = _byteorder_map[byteorder]

    @property
    def byteorder(self) -> ByteOrder:
        """
        Returns the byte order of the datastream.

        Returns:
            ByteOrder: The byte order of the datastream.
        """
        return ByteOrder(_byteorder_map.index(self._byteorder))

    @byteorder.setter
    def byteorder(self, value: int):
        """
        Sets the byte order for the datastream.

        Parameters:
        - value (int): The byte order value to set. One of the ByteOrder enumeration
            values.
        """
        self._byteorder = _byteorder_map[value]

    def read(self, size: int) -> bytes:
        """
        Reads up to `size` bytes from the backing stream.

        Args:
            size (int): The maximum number of bytes to read.

        Returns:
            bytes: The bytes read from the backing stream.
        """
        if self._backing_stream is None:
            raise ValueError("backing_stream has not been set.")

        return self._backing_stream.read(size)

    def size(self) -> int:
        """
        Returns the size of the backing stream.

        Returns:
            int: The size of the backing stream.
        """
        return len(self._backing_stream.getvalue())

    def remaining(self) -> int:
        """
        Returns the number of bytes remaining in the backing stream.

        Returns:
            int: The number of bytes remaining.
        """
        return self.size() - self.tell()

    def seek(self, offset: int, whence: int = io.SEEK_SET):
        """
        Change the stream position to the given offset.

        Args:
            offset (int): The offset to seek to.
            whence (int, optional): The reference position from where the offset is
                calculated. Defaults to io.SEEK_SET.
        """
        self._backing_stream.seek(offset, whence)

    def tell(self) -> int:
        """
        Returns the current position of the stream.

        Returns:
            int: The current position of the stream.
        """
        return self._backing_stream.tell()

    def close(self):
        """
        Closes the backing stream.
        """
        self._backing_stream.close()

    def write(self, data: bytes):
        """
        Writes the given data to the backing stream.

        Args:
            data (bytes): The data to be written.
        """
        if self._backing_stream is None:
            raise ValueError("backing_stream has not been set.")

        self._backing_stream.write(data)

    def clone(self) -> typing.Self:
        """
        Creates a clone of the current object.

        Returns:
            A new instance of the same class with the same byte order and contents.
        """
        return self.__class__(
            io.BytesIO(self._backing_stream.getvalue()), self.byteorder
        )

    def substream(self, start: int, end: int) -> typing.Self:
        """
        Returns a new instance of the same class, representing a substream of the
        current stream.

        Args:
            start (int): The starting index of the substream.
            end (int): The ending index of the substream.

        Returns:
            typing.Self: A new instance of the same class representing the substream.

        """
        return self.__class__(
            io.BytesIO(self._backing_stream.getvalue()[start:end]), self.byteorder
        )

    def peek(self, size: int) -> bytes:
        """
        Returns the next `size` bytes from the stream without advancing the position.

        Args:
            size (int): The number of bytes to peek.

        Returns:
            bytes: The next `size` bytes from the stream.

        """
        pos = self.tell()
        data = self.read(size)

        self.seek(pos)

        return data

    def seekpeek(self, offset: int, size: int) -> bytes:
        """
        Seeks to the specified offset in the data stream, reads the specified number of
        bytes, and then restores the original position.

        Args:
            offset (int): The offset from the current position to seek to.
            size (int): The number of bytes to read.

        Returns:
            bytes: The data read from the stream.

        """
        pos = self.tell()
        self.seek(offset)

        data = self.read(size)
        self.seek(pos)

        return data

    def search(self, data: bytes) -> int:
        """
        Searches for the given data in the backing stream.

        Args:
            data (bytes): The data to search for.

        Returns:
            int: The index of the first occurrence of the data , or -1 if not found.
        """
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

    def rsearch(self, data: bytes) -> int:
        """
        Searches for the given data in the reverse order within the backing stream.

        Args:
            data (bytes): The data to search for.

        Returns:
            int: The index of the first occurrence of the data, or -1 if not found.
        """
        pos = self.tell()
        remaining = self.remaining()

        while remaining > 0:
            self.seek(remaining, io.SEEK_CUR)
            chunk = self.read(len(data))

            if not chunk:
                self.seek(pos)

                return -1
            if chunk == data:
                index = self.tell() - len(data)
                self.seek(pos)

                return index

            remaining -= len(data)
        
        return -1

    def clear(self):
        """
        Clears the backing stream by truncating it to 0 bytes and resetting the stream
        position to the beginning.
        """
        self._backing_stream.truncate(0)
        self._backing_stream.seek(0)
