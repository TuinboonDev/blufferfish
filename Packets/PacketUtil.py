from Util import enforce_annotations

import struct

class Packet:
    def __init__(self, *packet_data):
        self.packet_data = packet_data

    def get(self):
        return list(self.packet_data)

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
        return bytes(data)

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
        return d

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
        return d

    def unpack_string(self, bytebuf, *args):
        length = self.unpack_varint(bytebuf)
        return bytebuf.recv(length).decode("utf-8")

    def unpack_encrypted_string(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        length = self.unpack_encrypted_varint(bytebuf, args[0])
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

    def unpack_encrypted_long(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">q", args[0].update(bytebuf.recv(8)))[0]

    def unpack_encrypted_unsigned_long(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">Q", args[0].update(bytebuf.recv(8)))[0]

    def unpack_long(self, bytebuf, *args):
        return struct.unpack(">q", bytebuf.recv(8))[0]

    def unpack_unsigned_long(self, bytebuf, *args):
        return struct.unpack(">Q", bytebuf.recv(8))[0]

    def unpack_encrypted_unsigned_short(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">H", args[0].update(bytebuf.recv(2)))[0]

    def unpack_uuid(self, bytebuf, *args):
        return bytebuf.recv(16)

    def unpack_encrypted_uuid(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return args[0].update(bytebuf.recv(16))

    def unpack_encrypted_remaining(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return args[0].update(bytebuf.recv(len(bytebuf)))

    def unpack_encrypted_location(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        position = self.decrypt_byte(bytebuf.recv(8), args[0])
        position_bits = ''.join(format(byte, '08b') for byte in position)
        position_x = int(position_bits[0:26], 2)
        position_z = int(position_bits[26:52], 2)
        position_y = int(position_bits[52:], 2)
        return (position_x, position_y, position_z)

    def unpack_encrypted_float(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">f", args[0].update(bytebuf.recv(4)))[0]

    def unpack_encrypted_double(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        return struct.unpack(">d", args[0].update(bytebuf.recv(8)))[0]

    def unpack_data(self, bytebuf, *args):
        length = self.unpack_varint(bytebuf)
        return bytebuf.recv(length)

    def unpack_encrypted_data(self, bytebuf, *args):
        if not args[0]:
            raise FileNotFoundError("Decryptor not set")
        length = self.unpack_encrypted_varint(bytebuf, args[0])
        return args[0].update(bytebuf.recv(length))

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
    def pack_byte(self, d: bytes):
        return d

    @enforce_annotations
    def pack_data(self, d: bytes):
        return self.pack_varint(len(d)) + d

    @enforce_annotations
    def write_string(self, s: str):
        s = bytes(s, encoding="utf-8")
        return self.pack_varint(len(s)) + s

    @enforce_annotations
    def pack_long(self, d: int):
        return struct.pack(">q", d)

    @enforce_annotations
    def pack_real_byte(self, d: int):
        return struct.pack(">B", d)

    @enforce_annotations
    def pack_location(self, location: tuple):
        x, y, z = location
        x &= 0x3FFFFFF  # 26 bits mask
        z &= 0x3FFFFFF  # 26 bits mask
        y &= 0xFFF      # 12 bits mask

        encoded_value = (x << 38) | (z << 12) | y

        if x & 0x2000000:
            x -= 0x4000000
        if z & 0x2000000:
            z -= 0x4000000
        if y & 0x800:
            y -= 0x1000

        return struct.pack('>Q', encoded_value)

    @enforce_annotations
    def pack_int(self, d: int):
        return struct.pack(">i", d)

    @enforce_annotations
    def pack_angle(self, d: float):
        return struct.pack(">B", int((d / 360.0) * 256.0) & 0xff)

    @enforce_annotations
    def pack_double(self, d: float):
        return struct.pack(">d", d)

    @enforce_annotations
    def pack_players(self):
        pass

    def pack_gamemode(self, gamemode):
        if gamemode == None:
            return int(-1).to_bytes(1, 'big', signed=True)
        elif gamemode == "survival":
            return int(0).to_bytes(1, 'big')
        elif gamemode == "creative":
            return int(1).to_bytes(1, 'big')
        elif gamemode == "adventure":
            return int(2).to_bytes(1, 'big')
        elif gamemode == "spectator":
            return int(3).to_bytes(1, 'big')

    def pack_float(self, d):
        return struct.pack(">f", d)