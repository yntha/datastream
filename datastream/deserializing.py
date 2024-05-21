import io
import typing
import struct


class DeserializingStream:
    def __init__(self, buffer: typing.Union[bytes, typing.IO[bytes]]):
        if isinstance(buffer, bytes):
            self.buffer = io.BytesIO(buffer)  # internally use a BytesIO object
        else:
            self.buffer = buffer