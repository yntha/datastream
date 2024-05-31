import io
import struct
import typing

from datastream.base import BaseStream, ByteOrder


class DeserializingStream(BaseStream):
    def __init__(
        self, buffer: bytes | typing.IO[bytes], byteorder: int = ByteOrder.NATIVE_ENDIAN
    ):
        if buffer is None:
            super().__init__(buffer, byteorder)
            
            return
        
        if not isinstance(buffer, io.BytesIO):
            if isinstance(buffer, io.IOBase):
                buffer = io.BytesIO(buffer.getvalue()) # type: ignore
            else:
                buffer = io.BytesIO(buffer) # type: ignore

        super().__init__(buffer, byteorder)
    
    def set(self, buffer: bytes | typing.IO[bytes]):
        if not isinstance(buffer, io.BytesIO):
            if isinstance(buffer, io.IOBase):
                self._backing_stream = io.BytesIO(buffer.getvalue()) # type: ignore
            else:
                self._backing_stream = io.BytesIO(buffer) # type: ignore
        else:
            self._backing_stream = buffer

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
    
    def read_uleb128(self) -> int:
        """
        Reads an unsigned LEB128 (Little-Endian Base 128) encoded integer from the data
        stream. Keep in mind that this method does not perform any bounds checking, so
        it is possible to read an arbitrarily large integer if a malformed sequence is
        read.
        
        Returns:
            int: The decoded unsigned integer.
        """
        return self.read_uleb128_safe(-1)

    def read_uleb128_safe(self, max_bytes: int = 16) -> int:
        """
        Reads an unsigned LEB128 (Little-Endian Base 128) encoded integer from the data
        stream.

        Args:
            max_bytes (int, optional): The maximum number of bytes to read before
                stopping. Defaults to 16.

        Returns:
            int: The decoded unsigned integer.
        """
        if max_bytes == 0:
            return 0
        
        decoded = self.read_uint8()

        if decoded < 0x7F:
            return decoded

        decoded &= 0x7F
        shift_mod = 1

        while max_bytes != 0 and (current_byte := self.read_uint8()) & 0x80:
            decoded += (current_byte & 0x7F) << shift_mod * 7
            shift_mod += 1
            max_bytes -= 1

        return decoded + (current_byte << shift_mod * 7) # type: ignore
    
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
    
    def read_sleb128_safe(self, stop_after: int = 5) -> int:
        """
        Reads a signed LEB128 (Little-Endian Base 128) encoded integer from the data
        stream.

        Args:
            stop_after (int, optional): The maximum number of bytes to read before
                stopping. Defaults to 5.

        Returns:
            int: The decoded signed integer.
        """
        if stop_after == 0:
            return 0

        decoded = self.read_uint8()
        shift_mod = 1

        if decoded < 0x7F:
            return decoded
        
        decoded &= 0x7F

        while stop_after != 0 and (current_byte := self.read_uint8()) & 0x80:
            decoded += (current_byte & 0x7F) << shift_mod * 7
            shift_mod += 1
            stop_after -= 1
        
        decoded += (current_byte << shift_mod * 7) # type: ignore

        if current_byte & 0x40: # type: ignore
            decoded |= -(1 << (shift_mod * 7) + 7)

        return decoded
