import io
import struct
import typing

from datastream.base import BaseStream, ByteOrder


class DeserializingStream(BaseStream):
    def __init__(
        self, buffer: bytes | typing.IO[bytes], byteorder: int = ByteOrder.LITTLE_ENDIAN
    ):
        if not isinstance(buffer, io.BytesIO):
            if isinstance(buffer, io.IOBase):
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

    def read_bool(self) -> bool:
        return bool(self.read_uint8())
    
    def read_uleb128(self, p1: bool = False) -> int:
        """
        Reads an unsigned LEB128 (Little-Endian Base 128) encoded integer from the data
        stream. Keep in mind that this method does not perform any bounds checking, so
        it is possible to read an arbitrarily large integer if a malformed sequence is
        read.

        Args:
            p1 (bool, optional): Whether this is ULEB128p1. Defaults to False.
        
        Returns:
            int: The decoded unsigned integer.
        """
        return self.read_uleb128_safe(p1, -1)

    def read_uleb128_safe(self, p1: bool = False, stop_after = 5) -> int:
        """
        Reads an unsigned LEB128 (Little-Endian Base 128) encoded integer from the data
        stream.

        Args:
            p1 (bool, optional): Whether this is ULEB128p1. Defaults to False.
            stop_after (int, optional): The maximum number of bytes to read before
                stopping. Defaults to 5.

        Returns:
            int: The decoded unsigned integer.
        """
        decoded = self.read_uint8()

        if decoded < 0x7F:
            return decoded + int(p1)

        decoded &= 0x7F
        shift_mod = 1

        while stop_after != 0 and (current_byte := self.read_uint8()) & 0x80:
            decoded += (current_byte & 0x7F) << shift_mod * 7
            shift_mod += 1
            stop_after -= 1

        return decoded + (current_byte << shift_mod * 7) + int(p1)
    
    def read_sleb128(self) -> int:
        """
        Reads a signed LEB128 (Little-Endian Base 128) encoded integer from the data
        stream. Keep in mind that this method does not perform any bounds checking, so
        it is possible to read an arbitrarily large integer if a malformed sequence is
        read.

        Returns:
            int: The decoded signed integer.
        """
        return self.read_sleb128_safe(-1)
    
    def read_sleb128_safe(self, stop_after = 5) -> int:
        """
        Reads a signed LEB128 (Little-Endian Base 128) encoded integer from the data
        stream.

        Args:
            stop_after (int, optional): The maximum number of bytes to read before
                stopping. Defaults to 5.

        Returns:
            int: The decoded signed integer.
        """
        decoded = self.read_uint8()
        shift_mod = 1

        if decoded < 0x7F:
            return decoded
        
        decoded &= 0x7F

        while stop_after != 0 and (current_byte := self.read_uint8()) & 0x80:
            decoded += (current_byte & 0x7F) << shift_mod * 7
            shift_mod += 1
            stop_after -= 1
        
        decoded += (current_byte << shift_mod * 7)

        if current_byte & 0x40:
            decoded |= -(1 << (shift_mod * 7) + 7)

        return decoded
