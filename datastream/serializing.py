import io
import struct
import typing

from datastream.base import BaseStream, ByteOrder


class SerializingStream(BaseStream):
    def __init__(
        self,
        buffer: typing.IO[bytes] | None = None,
        byteorder: int = ByteOrder.NATIVE_ENDIAN,
    ):
        if buffer is None:
            buffer = io.BytesIO()

        super().__init__(buffer, byteorder)
    
    def write_format(self, fmt: str, value: typing.Any):
        self.write(struct.pack(self._byteorder + fmt, value))
    
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
