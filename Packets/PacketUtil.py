import struct

class ByteBuffer:
    def __init__(self, bytes):
        self.buffer = bytearray(bytes)

    def __len__(self):
        return len(self.buffer)

    def recv(self, length):
        data = self.buffer[:length]
        self.buffer = self.buffer[length:]
        return data

    def unpack_varint(self):
        d = 0
        bytes_length = 0
        for i in range(5):
            b = ord(self.recv(1))
            d |= (b & 0x7F) << 7*bytes_length
            bytes_length += 1
            if not b & 0x80:
                break
        return d, bytes_length

    def unpack_encrypted_varint(self, decryptor):
        if not decryptor:
            raise FileNotFoundError("Decryptor not set")
        d = 0
        bytes_length = 0
        for i in range(5):
            b = ord(decryptor.update(self.recv(1)))
            d |= (b & 0x7F) << 7*bytes_length
            bytes_length += 1
            if not b & 0x80:
                break
        return d, bytes_length

    def unpack_string(self, buf):
        length, length_bytes = self.unpack_varint()
        return buf.recv(length).decode("utf-8")

    def unpack_encrypted_string(self, decryptor):
        if not decryptor:
            raise FileNotFoundError("Decryptor not set")
        length, length_bytes = self.unpack_encrypted_varint(decryptor)
        return decryptor.update(self.recv(length)).decode("utf-8")

    def decrypt_byte(self, b, decryptor):
        return decryptor.update(b)

    def unpack_varint_bytes(self, byte_string):
        result = 0
        shift = 0
        for byte in byte_string:
            value = byte & 0x7F
            result |= value << shift
            shift += 7
            if not byte & 0x80:
                break
        return result

def pack_varint(d):
    o = b""
    while True:
        b = d & 0x7F
        d >>= 7
        o += struct.pack("B", b | (0x80 if d > 0 else 0))
        if d == 0:
            break
    return o

def pack_data(d):
    return pack_varint(len(d)) + d

def write_string(s):
    s = bytes(s, encoding="utf-8")
    return pack_varint(len(s)) + s

def unpack_varint(buf):
    d = 0
    bytes_length = 0
    for i in range(5):
        b = ord(buf.recv(1))
        d |= (b & 0x7F) << 7*bytes_length
        bytes_length += 1
        if not b & 0x80:
            break
    return d, bytes_length

def unpack_encrypted_varint(buf, decryptor):
    if not decryptor:
        raise FileNotFoundError("Decryptor not set")
    d = 0
    bytes_length = 0
    for i in range(5):
        b = ord(decryptor.update(buf.recv(1)))
        d |= (b & 0x7F) << 7*bytes_length
        bytes_length += 1
        if not b & 0x80:
            break
    return d, bytes_length