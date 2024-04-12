from Util import enforce_annotations

import struct

class ByteBuffer:
    @enforce_annotations
    def __init__(self, bytes: bytes):
        self.buffer = bytearray(bytes)

    def __len__(self):
        return len(self.buffer)

    @enforce_annotations
    def recv(self, length: int):
        data = self.buffer[:length]
        self.buffer = self.buffer[length:]
        return data

class Unpack:
    def unpack_varint(self, bytebuf, *args):
        d = 0
        bytes_length = 0
        for i in range(5):
            b = ord(bytebuf.recv(1))
            d |= (b & 0x7F) << 7*bytes_length
            bytes_length += 1
            if not b & 0x80:
                break
        return d, bytes_length

    def unpack_encrypted_varint(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        d = 0
        bytes_length = 0
        for i in range(5):
            b = ord(args[0].update(bytebuf.recv(1)))
            d |= (b & 0x7F) << 7*bytes_length
            bytes_length += 1
            if not b & 0x80:
                break
        return d, bytes_length

    def unpack_string(self, bytebuf, *args):
        length, length_bytes = self.unpack_varint(bytebuf)
        return bytebuf.recv(length).decode("utf-8")

    def unpack_encrypted_string(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        length, length_bytes = self.unpack_encrypted_varint(bytebuf, args[0])
        return args[0].update(bytebuf.recv(length)).decode("utf-8")

    def unpack_byte(self, bytebuf, *args):
        return bytebuf.recv(1)

    def unpack_encrypted_byte(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return args[0].update(bytebuf.recv(1))

    def unpack_short(self, bytebuf, *args):
        return struct.unpack(">h", bytebuf.recv(2))[0]

    def unpack_unsigned_short(self, bytebuf, *args):
        return struct.unpack(">H", bytebuf.recv(2))[0]

    def unpack_encrypted_short(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">h", args[0].update(bytebuf.recv(2)))[0]

    def unpack_encrypted_unsigned_short(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">H", args[0].update(bytebuf.recv(2)))[0]

    def decrypt_byte(self, b, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return args[0].update(b)

    @enforce_annotations
    def unpack_varint_bytes(self, byte_string: bytes):
        result = 0
        shift = 0
        for byte in byte_string:
            value = byte & 0x7F
            result |= value << shift
            shift += 7
            if not byte & 0x80:
                break
        return result

class Pack:
    @enforce_annotations
    def pack_varint(self, d: int):
        o = b""
        while True:
            b = d & 0x7F
            d >>= 7
            o += struct.pack("B", b | (0x80 if d > 0 else 0))
            if d == 0:
                break
        return o

    @enforce_annotations
    def pack_data(self, d: bytes):
        return self.pack_varint(len(d)) + d

    @enforce_annotations
    def write_string(self, s: str):
        s = bytes(s, encoding="utf-8")
        return self.pack_varint(len(s)) + s