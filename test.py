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
        },
        "S2C": {
            0x02: [{"entity_id": PacketPayloads.VARINT}, {"head_yaw": PacketPayloads.BYTE}, {"head_pitch": PacketPayloads.BYTE}],
        }
    }
    }

packet_id = 0

packet_data = {}

for payload in PacketMap.map["blabla"]["C2S"][packet_id]:
    for key, value in payload.items():
        if list(payload.keys())[0] == "encrypted":
            print("yes")
            continue
        else:
            print("no")
        packet_data[key] = value()

print(packet_data)

#amazing packet idea

def __send(packet_id, *args):
    packet = PacketMap.map["blabla"]["S2C"][packet_id]

    for x in packet:
        print(x)

__send(2, "a", "b", "c")

