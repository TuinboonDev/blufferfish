import struct

def unpack_varint(s):
    d = 0
    bytes_length = 0
    for i in range(5):
        b = ord(s.recv(1))
        d |= (b & 0x7F) << 7*i
        bytes_length += 1
        if not b & 0x80:
            break
    return d, bytes_length

decryptor = None

def unpack_encrypted_varint(s):
    if not decryptor:
        raise Exception("Decryptor not set")
    d = 0
    bytes_length = 0
    for i in range(5):
        b = ord(decryptor.update(s.recv(1)))
        d |= (b & 0x7F) << 7*i
        bytes_length += 1
        if not b & 0x80:
            break
    return d, bytes_length

def decrypt_byte(b):
    return decryptor.update(b)

def unpack_varint_bytes(byte_string):
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