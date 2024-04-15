def unpack_varint(a):
    return "lol"

def pack_varint(a):
    pass

Unpack = {}
Pack = {}
class PacketPayloads:
    class Unpack:
        class ENCRYPTED:
            VARINT = unpack_varint
            STRING = unpack_varint
            BYTE = unpack_varint
            SHORT = unpack_varint
            UNSIGNED_SHORT = unpack_varint

        class UNENCRYPTED:
            VARINT = unpack_varint
            STRING = unpack_varint
            BYTE = unpack_varint
            UNSIGNED_SHORT = unpack_varint

    class Pack:
        VARINT = unpack_varint
        BYTE = unpack_varint

class PacketMap:
    Pack = PacketPayloads.Pack
    Unpack = PacketPayloads.Unpack
    map = {"blabla": {
        "C2S": {
            0x00: [{"encrypted": True}, {"entity_id": Pack.VARINT}, {"head_yaw": Pack.BYTE}],
            0x01: [{"entity_id": Pack.VARINT}, {"head_pitch": Pack.BYTE}]
        },
        "S2C": {
            0x02: [{"entity_id": Unpack.UNENCRYPTED.VARINT}, {"name": Unpack.UNENCRYPTED.BYTE}, {"head_pitch": Unpack.UNENCRYPTED.BYTE}],
        }
    }
    }

packet_id = 0

packet_data = {}

for payload in PacketMap.map["blabla"]["C2S"][packet_id]:
    for key, value in payload.items():
        if list(payload.keys())[0] == "encrypted":
            #print("yes")
            continue
        else:
            pass
            #print("no")
        packet_data[key] = value("a")


#amazing packet idea

class Packet:
    def __init__(*packet_data):
        return packet_data

class funky_packet(Packet):
    def __new__(self, entity_id, name):
        return super().__init__(entity_id, name)



def __send(packet):
    #print(packet)
    packet_sequence = PacketMap.map["blabla"]["S2C"][2]

    #print(packet_sequence)
    #Copilot do you have a Good way to get packet id from packet class?
    packet_id = packet.__class__.__name__
    #print(packet_id)


    for x in range(len(packet)):
        pass
        #print(packet[x])
        #print(list(packet_sequence[x].values())[0](packet[x]))

a = funky_packet(1, "Tuinboon")

__send(a)

print("\n\n\n\n")

class Packet:
    def __init__(self, *packet_data):
        self.packet_data = packet_data

    def get(self):
        return self.packet_data

class StatusResponse(Packet):
    def __init__(self, server_data: dict, a):
        return super().__init__(server_data, a)

st = StatusResponse({"response": "hello"}, "a")
print(st.get())

"""def __send(self, packet, gamestate: GameStates, encryption: Encryption):
        packet_id_map = {v: k for k, v in GameStates[gamestate.get_gamestate()]["S2C"].items()}

        packet_class = type(packet)

        try:
            final_packet = Pack.pack_varint(packet_id_map.get(packet_class))
        except TypeError as e:
            raise TypeError(f"Packet {packet_class} is not in the PacketMap") from e

        for key in list(packet.__dict__.keys()):
            final_packet += packet.__dict__[key]

        if packet_class.__name__ == "SetTabListHeaderFooter":
            print(len(final_packet))
            for x in final_packet:
               print(hex(x))
            print("\n")
            pass

        try:
            if encryption is not None:
                self.socket.send(encryption.update(Pack.pack_varint(len(final_packet)) + final_packet))
            else:
                self.socket.send(Pack.pack_varint(len(final_packet)) + final_packet)
            return True
        except ConnectionAbortedError as e:
            #TODO: add custom client disconnect error
            print("Client disconnected, shutting down keepalive thread")
            sys.exit()
        except Exception as e:
            print(f"Error while sending packet: {e}")
            return False"""

import struct

def encode_coordinates(x: int, z: int, y: int):
    # Ensure values are within range
    x &= 0x3FFFFFF  # 26 bits mask
    z &= 0x3FFFFFF  # 26 bits mask
    y &= 0xFFF      # 12 bits mask

    # Combine the values into a single 64-bit integer
    encoded_value = (x << 38) | (z << 12) | y

    # If the highest bit of each coordinate is set (indicating negative value), convert to two's complement
    if x & 0x2000000:
        x -= 0x4000000
    if z & 0x2000000:
        z -= 0x4000000
    if y & 0x800:
        y -= 0x1000

    return struct.pack('>Q', encoded_value)

class Player:
    def __init__(self, uuid, name, session):
        self.uuid = uuid
        self.name = name
        self.session = session

player = Player("a", "b", {"properties": [{"name": "a", "value": "b", "signature": "c"}]})

player_actions = [{"uuid": player.uuid, "name": player.name, "show": True, "properties": {"name": player.session["properties"][0]["name"],
                                                                                                        "value": player.session["properties"][0]["value"],
                                                                                                        "is_signed": True,
                                                                                                        "signature": player.session["properties"][0]["signature"]}}]

number_of_players = len(player_actions)


import struct

a = struct.pack(">d", 1.0)

print("a")
print(a)