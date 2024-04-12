def unpack_varint():
    return "lol"

class PacketPayloads:
    VARINT = unpack_varint
    STRING = 1
    BYTE = unpack_varint
    SHORT = 3

class PacketMap:
    map = {"blabla": {
        "C2S": {
            0x00: [{"encrypted": True}, {"entity_id": PacketPayloads.VARINT}, {"head_yaw": PacketPayloads.BYTE}],
            0x01: [{"entity_id": PacketPayloads.VARINT}, {"head_pitch": PacketPayloads.BYTE}]
        }
    }
    }

packet_id = 0

for payload in PacketMap.map["blabla"]["C2S"][packet_id]:
    for key, value in payload.items():
        if list(payload.keys())[0] == "encrypted":
            print("yes")
            continue
        else:
            print("no")
        print(f"key: {key}, value: {value()}")

#amazing packet idea