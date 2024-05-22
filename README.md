# datastream
[![Lint and test](https://github.com/yntha/datastream/actions/workflows/python-app.yml/badge.svg)`](https://github.com/yntha/datastream/actions/workflows/python-app.yml)

Because `construct` was too complicated. This is a simple and easy to use library that provides two classes. One class serializes data, and the other one deserializes. These classes behave like streams in which they have `read`, `write`, `close` among other stream related functions. The goal of this library is to be as simple as possible while providing flexibility.

To import the library, use the following:
```python
from datastream import SerializingStream, DeserializingStream, ByteOrder
```

The stream classes support serializing/deserializing the standard data types:
| Data Type | Description | [Serializer](datastream/serializing.py#L8) | [Deserializer](datastream/deserializing.py#L8)
| --- | --- | ---| --- |
| `int8_t` | Signed 8-bit number | [`write_int8(value: int)`](datastream/serializing.py#L52) | [`read_int8() -> int`](datastream/deserializing.py#L41) |
| `uint8_t` | Unsigned 8-bit number | [`write_uint8(value: int)`](datastream/serializing.py#L55) | [`read_uint8() -> int`](datastream/deserializing.py#L44) |
| `int16_t` | Signed 16-bit number | [`write_int16(value: int)`](datastream/serializing.py#L46) | [`read_int16() -> int`](datastream/deserializing.py#L35) |
| `uint16_t` | Unsigned 16-bit number | [`write_uint16(value: int)`](datastream/serializing.py#L49) | [`read_uint16() -> int`](datastream/deserializing.py#L38) |
| `int32_t` | Signed 32-bit number | [`write_int32(value: int)`](datastream/serializing.py#L40) | [`read_int32() -> int`](datastream/deserializing.py#L29) |
| `uint32_t` | Unsigned 32-bit number | [`write_uint32(value: int)`](datastream/serializing.py#L43) | [`read_uint32() -> int`](datastream/deserializing.py#L32) |
| `int64_t` | Signed 64-bit number | [`write_int64(value: int)`](datastream/serializing.py#L34) | [`read_int64() -> int`](datastream/deserializing.py#L23) |
| `uint64_t` | Unsigned 64-bit number | [`write_uint64(value: int)`](datastream/serializing.py#L37) | [`read_uint64() -> int`](datastream/deserializing.py#L26) |
| `float` | 32-bit floating point number | [`write_float(value: float)`](datastream/serializing.py#L58) | [`read_float() -> float`](datastream/deserializing.py#L47) |
| `double` | 64-bit floating point number | [`write_double(value: float)`](datastream/serializing.py#L61) | [`read_double() -> float`](datastream/deserializing.py#L50) |

Additionally, the stream classes also provide the following non-standard data types:
| Data Type | Description | [Serializer](datastream/serializing.py#L8) | [Deserializer](datastream/deserializing.py#L8)
| --- | --- | ---| --- |
| `bool` | True/False value encoded as a single byte | [`write_bool(value: bool)`](datastream/serializing.py#L64) | [`read_bool() -> bool`](datastream/deserializing.py#L53) |
| `uleb128` | Variable sized unsigned 128-bit number | [`write_uleb128(value: int)`](datastream/serializing.py#L67) | [`read_uleb128() -> int`](datastream/deserializing.py#L56) |
| | | [`write_uleb128_safe(value: int, max_bytes: int = 16)`](datastream/serializing.py#L78) | [`read_uleb128_safe(max_bytes: int = 16) -> int`](datastream/deserializing.py#L68) |
| `sleb128` | Variable sized signed 128-bit number | [`write_sleb128(value: int)`](datastream/serializing.py#L99) | [`read_sleb128() -> int`](datastream/deserializing.py#L95) |
| | | [`write_sleb128_safe(value: int, max_bytes: int = 16)`](datastream/serializing.py#L110) | [`read_sleb128_safe(max_bytes: int = 16) -> int`](datastream/deserializing.py#L107) |

Finally, the stream classes also provide the following utility functions:
| Function | Description |
| --- | --- |
| [`read(size: int) -> bytes`](datastream/base.py#L64) | Reads up to `size` bytes from the backing stream. |
| [`write(data: bytes)`](datastream/base.py#L120) | Writes the given data to the backing stream. |
| [`size() -> int`](datastream/base.py#L76) | Returns the size of the backing stream. |
| [`seek(offset: int, whence: int = io.SEEK_SET)`](datastream/base.py#L94) | Change the stream position to the given offset. |
| [`tell() -> int`](datastream/base.py#L105) | Returns the current position of the stream. |
| [`close()`](datastream/base.py#L114) | Closes the backing stream. |
| [`remaining() -> int`](datastream/base.py#L85) | Returns the number of bytes remaining in the backing stream. |
| [`clone() -> typing.Self`](datastream/base.py#L129) | Returns a new instance of the same class with the same byte order and contents. |
| [`substream(start: int, end: int) -> typing.Self`](datastream/base.py#L140) | Returns a new instance of the same class, representing a substream of the current stream. |
| [`peek(size: int) -> bytes`](datastream/base.py#L157) | Returns the next `size` bytes from the stream without advancing the position. |
| [`seekpeek(offset: int, size: int) -> bytes`](datastream/base.py#L175) | Seeks to the specified offset in the data stream, reads the specified number of bytes, and then restores the original position. |
| [`search(data: bytes) -> int`](datastream/base.py#L196) | Searches for the given data in the backing stream. |
| [`rsearch(data: bytes) -> int`](datastream/base.py#L223) | Searches for the given data in the reverse order within the backing stream. |
| [`clear()`](datastream/base.py#L252) | Clears the backing stream by truncating it to 0 bytes and resetting the stream position to the beginning. |