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
    print(packet)
    packet_sequence = PacketMap.map["blabla"]["S2C"][2]

    #print(packet_sequence)
    #Copilot do you have a Good way to get packet id from packet class?
    packet_id = packet.__class__.__name__
    print(packet_id)


    for x in range(len(packet)):
        pass
        #print(packet[x])
        #print(list(packet_sequence[x].values())[0](packet[x]))

a = funky_packet(1, "Tuinboon")

__send(a)

print("\n\n\n\n")

class Packet:
    def __init__(self, *packet_data):
        self.packet_data = packet_data[0]

    def get(self):
        return self.packet_data

class StatusResponse(Packet):
    def __init__(self, server_data: dict):
        return super().__init__(server_data)

print(StatusResponse("a").get())

print(type(StatusResponse("")))


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

for x in b"\x861{'version': {'name': 'BlufferFish 1.20.4', 'protocol': 765}, 'players': {'sample': [{'name': 'BlufferFish', 'id': 'd552a0a7-b211-47c1-9396-5f39dcfedc73'}, {'name': 'Tuinboon', 'id': 'd552a0a7-b211-47c1-9396-5f39dcfedc73'}], 'max': 5, 'online': -5}, 'description': {'text': '\xc2\xa73Bluffer\xc2\xa7eFish'}, 'favicon': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAABDZSURBVHgB7VsLeE1X2n7J5UQiRETcEokEIa5BXCIklGLaqMuMFj9Sl6l20KGouJUpajqe6mhpXVphWqMXjBraqKCCiWBIRFQiFxKXiFyQROS2/+9b+5yTfc7Z5zi56PP/M33zfM/Ze621117ft9f6bmsF+BX/3aiHXx5ORP2I+hN1IconmkNUjv9guBDNIIoiKiKSjKg3ngGo46lE+UTpfI3qotYdAN2INhM9hCnTSgpVPPMR0SdEdqgFtGOXFJSP6kLLuLITa4XQjmgfUSUUjLo62ktvBPtK+2cMkL6ZFqQmgBDUwaxQYZ4pXa2t7VP6cjG6j+SRkeLYaaY9r++3iRYRabigXr16eN6vORYN64gQ32awqS+rnRPX76k9r9RJDVEDaD9SpErVKrX2TxPAPKIdRmXmhOANeY13gFyPV3q1wfLh/ujUohHqAE2JhhIdJ1KTnobG9QrUmX+1nnq5ZQHU0zIL64TAU1Ywb29TH9+/PghDOrijDrGL6DdEfyOaYlQ3chqwl34bqDxnlnnG02ZAdYTwT6JjRENKKyqxOioJ/bxd4Wj/1FcwaPyYROSrKFtHdAXy2uXf57Tlj42erUc2dPPGGjBfLRCz4SqKxVgxOhJFQ6vIBrd3l4rWj5WkjeP1dG7hUGnxsE6Sn7uzJatgiVi5dtK98DzpHDPjCkddoyZCCNUKIeqNQVJIu2aqTJGilFq6N5K6+bWUgnu1lQYF+ki9u3pKragM5gVxhhTOu7VlvtqeoLbzHSpV4YrlwEI4SDSEb9wa2uN+YWnVS8kyDOztg+EDO4rfHp1awdnJQfV9j0vKcOFKJs5cyMB3xxJx+t/potycqkc1p32NXGErhcAmNImopa7SxbkB5k4ZiJkv94dHCxfUBBlZuYheuBvTL6SZ1FWQLrFVH5dZWKWhjGGFYmRlyGtVMO+gscVb0wdjARELwRwk+pv7p/0oL6/AxhVjYWdrY9LGOy5NlflXIT77XMjv7g7Zm/ycaDks81JzmJsJvwcKtmmdqJ6dPfDF+v9BJ9/mT+3v/OVMBI77QFyf2zsfpAcMG+w7ByzebfLc6jZuWH7zvu42g6gVkT3RVSJ/WIANagFyrS6tBG7Q5WhleRh99Az6DaHp/tVfp6KFm3WOULOmDXEvtxBBAd6Y9tt+pCvk8lvZDyDtjYPDO9+YPrRuAgaseRlPSitw+oLQDyx45ouVDgdgKZbeWSfhsFmdQIPD2D6oDTJu5WPd8LX4tFQlWjbqf9XHUVi58QfdLXuLvYiyLPVfH9UHm7ibkGN4AVZ85DNfN2m5+O80beNQG7j8eNkq5hnvzB6OVXNH6G7ZDf0WVXqOfxcQ5RId0TVSLgFvos+IfIhOQR1sqz6G7JePhPzlWSNNjqVlYLIWGEcTgdau5Lq0Frcnz6XiD6v2CivgxeWWQGve3LQ3N7NC+rRDwcPHOBvPo4EH5I/MdACyt8lamJXLX4gqlALYQEQ9i4CD7fdxogdG/fOnuEAUDHmtuWifGcSVxd7ueGNRGOpHJ8KcEJj5QyeSkJNXiIlhvWCJeTWFZ82yGtK/Aw7/lIQ7OZyGEGPj2EEXmKRoBSF0g04ALSA7D7ol4UU0BrIPbmxzeKpz0oKFEwA5BIYtBUBx++bBtV97mdmj6kLwCO0smF808zmaAU1QE+bzHxQj6Xo20kjzN3TUoIGDYe7EhsYS0scX27+JRUVFpa64AHJIPAUKxahTguHQKjHy33E8xSDa5IdWQh3Tibbzxdszh2DdwjAFE3GyDjDDhFlYYD6eZtC89/6Bn+JSUVkp6at+M9gfHy0dC582TQ0eWbbhENZ8clR3O5Zov3G3uhmwmqhDc2cNEhaPQItGDjiVmoMn5UJ6oUSsWbgn4yWxiciTfHbsfH8inBw1VTW85i3MBJ1OsJb5XWQTR7/xGa7fuC+cfSVSMnKw+ctTQqf0UPTbs7Mntvz9DEpkJcqOiEkiR6cgxBqmwEXY3lnBvrj09nD4NHXSteMs7kmiFxTPdoac2cWEsJ5wb+psMu6Tnk2x1L2xSbmqdbDAfGpvX0xfsgclT8pha2eH1+f+ETu/+hZ7D0Vh0tRXRWxRTlN91vKvcenqLf2jLo0aYA75IlqEasdsIoBAIjH6kf56tx3exPyVJSMwb3AHXVEbyDH/nyAvnRm6itmTBkIN7287hrX3HmB+I0dYFMJT1vyba/YLBpnRA1HRWLN+A8LGjMPgYc/jo22f42D0CSEY/tLz3ztg0EX42L7K21eMX8FLYDjRS3yzamRnNG9UFZWxYhveqQVaN26AM2n38bisgotDIJw94W83ofAV86eFQg0ezV2Ewpu+Yhy8SCmpLocsStZ+/INZ5vMKijFj6R5RNJG+9muz54rrO7dvoSAvH41dXODZxgsF+Xk4fzYWmbfzMWfyQL1ibEJj//F0MjLvsA4ET0dW7GweSriAZwBvTkBjWx92Nup+0cwgH5xfNAy+bvol0ROyv4CwwV1gDoOI6X9unQmK7wUz0nsTTBvtjzPLPCMp9a6+eNx4+QNm3shATz9f9Onihzt3bouyfkHyLKwg5ZiWlWfQ3fBgP90lfzReyvzQO9AKQKwLVnj+a39Ay2Xf4cVPY7A++hopwvs6RQhvVyckLRmJBUP8DDoPohlgLVZk5oqozSKMrEQDjb3+urCwUPza2lWVlZeWiV8n56okMucQlBg6oIM+rtB1C9my/YHdQwPbcfdhCQ4l3REkXkZp7D5erngvrBsGtWuGv4zujrziJ/g8NkPUc7RnDVhTr94se6C8hsLVGo0NNDGRbT1dUZ/GwGYv9nQMrf2xaNmqFeISr8HO3g4tWrYS7fZ/tUf/TOd2hpFnUEBbJB9Ziqy7BUKRvkbK8uYdsU/yJs8AEXMO79Qcm8f3xO8CPGiqV0mznF58Jj0X70f/rC+TtO4Dmz9HB+s2cJZ+cFj8ToWFfBUrQyPr4NrYUTg1jG2fbMKZmJPi2tPLS888l+3+W6S4Dhvcmda9qdJt5+WG0L7tMGJQR/JAe+qKfXgGiFi1O3llrwe3E8S4mV+MS6SgjqXk4Pq9R1g0tKO+s+yHJVoBVJm4MkpixJMJ6tW1jUmI+ajoCfZGxVtKY1VB5zwpZsIHEaPR73cfUshbhrChoZgwJRxjSR8UPnqE2DOnsH3zJvINJKG0P1w2xqA7DqV59unASnXPoYu62xQWgPBeHIwUYJsmjoJGdTV1WLTWAA0aVH39Oe/uE07HnMnB2Lh8nEH7+J9vYTINMBIq6OsNnM2AJSGwc7N19XhMj9gjzOHunTsEKaGxs8UWygv4eFataA6lO1Io/aTU7Mbzh8y18KskWA/t7hakiqqn7Gxkp7K0rNKkfZfLWerMT+ojKGNkZ9M6I2dpyuhAXDsSgVFDDNuyfhhMUzv223mYOtpwO9He9qnRvi3PAJ7PjiXlFQY12Y9KcPJ6jlj/17IfgnL5QgkynLXr/kFhib79R5TDmzImUGR4DUDr2mXtftNXE+Nlvdtg7fdXsOZIkgjPdqgJgaGdCT6ebjjw6QzkU7h7JfmOsPVt6Yu7qqx5RqvmjXEtKgLpCrNorARZAOzfOybTOt8Ucx2xGbk4Qes+i9aKErypqROAm5NshnILigzaBFqZw+MvXuDhgvD1RxF/Szgo+IK+1oSR3fH8wYsWhcBoQi5ucG8fWAOOD4zzDqwE123lvI6sBHkELQ9cvg0mYzjQwAI8mmChQgna1JenFsfbj2gWODdUyembYZ79gCNn0pBDX71Mu4S6+7XEjj9PQoA/6ZsBHU2jSBUhVBccRLEZNFKCySyAa1BsNbk31CDIxw39vZuK3570pXT7e8Wk/CIOJGDL6VRxz1FZ/LXbCO7lYxXzuwf4IfI0ve6BvL1nS8JdMmsolrw+TCgxAybrUAiJyXfRLex9YSmM8Fd+qz5pmLx8JNo3c1btJPV+IcZsP43Ltw0j4phzaYYCsBDYvEKK7MvXtlG25qr2q0+kr67iSNWxEPb9GG/MPLuUHNRtYQHoIxTJjCmIjMvAvL0XUfBY72L+C3K+zfP7mKuImDVU+yZ15i+/GoKuNGheOIe2/V7k/7uTslTb+NDDghC+PnwR22n5lJOb7uRoLzJLfm3dEUDmsm8PL5N+D5+4qrvkbBbr22TIS19kSs/qak+Q1u/gXjUDikhjvv1dglCOCvyZaCnRu0QRPAM40vL8V4rZNZ+TniPiaB1MNjyqKYTxJ38G+5Vqx1Q0tFzZ45vwQgCeD+4o4gJtgpTxNZGBq8kWnW0ab6s0mhzohV2T5fj5Ok35l7acQlL2Q13bbMiebJT2nv1JTpDiM0pYTDufajKYq5QmW5hyV+T/RERoBdhzKydd4+XhCqm+BmWOPlgfOhtLkk2z7m9SKHyibVukJiejqKjIpJ49Qx/aNUpO16f4OLmRYiwABn+gF5rQdMpe8xJ2nk3HW/+Ix8OqqCqGaCJMNxlOkERCIqGCGmyK6Dw3RuKlaLj59qe9czvcpPDX8csv0H6l6TZf0fZIlE6Zioy0VCQmJOD7QwcRcywaWZk3jZvynuFzxoU6V0nM0PziUoRtjcHMPeeVzK+BHMCZ7LBQbHcyEqbYQApuv7MD7eTmQQ2VlZVIpYzu7oMX9G2k+jQRG9MHqmcjqNjOSzDPaOPlDbcly4hZ080npxnhsN+1E94+vnhx9BhsogxRQuoNHDgSjdaeBkstEhbA+X3jA4wcDz9npr2GNkIi1A4nhBsdZHB20kg9/T2kkEBfqX8Pb6m9VzPJsYG9vt6vXWupMC9Jyi8pkfJKJSk+JUNKunFLXKtR4fYdagciqDzSoN3F5HRx8EIxFl7C82FhOzBS0fg4UWsz7Yb+kXwHtUHMtLOTgkMHSxqNxtLJDgMaETbKLLM1FcK9olKpra+vuXemQ85yCyjPB6wgYl/3J8jbRmpG0YG0+uENKqc4xf58WRle69wN+yhbeyHuLBLiLyEl+ZpIYRUXF9OGhQ1cmzZFs2bu8Ovkj8C+/eDftSuqi1IKhxlOMwzzS7wcGMsSE5CeqlfKbK3IPmMj5O0/Jj67wLsyT1AdlJs5I0R2YiZk8yKkvHjFymp/1ZqQuZkwtepr/xuGU3425I3do6guJPXjp8oDSaxxsvF/RAhz5KnuhbqAFcwzXoQ8pfTrbfa8BVLO4/JnLoTcTZ9K0tNPrz1T5hlX5ebiZEaGTgi+7dtLl1LSnxnzsQlJUreAAGF96lwI1WCewcqG96VGQVY0CdAKgZSfNOethdLPWdl1xnj6vXxp/uKlksbBQT/jyDol15kQqsm8GtjJWg3FknBv3kKaNedNYaNrynhiWqa0cOkKiXaEJGXfROxC2krWHea0SgDptWBeh1GAuv0P7NdfWv7uWulQ9EnpVkGRWYZv5D6UDh+PkZZR26DgQcbOjZKGKMZeeyFI8n+K1IZ5RrrclbAOfCD6tDmBUI5f6tErUAoaGCL1DQqW/Lt0E2UWGD5O9FvI/wnC9xzW29aZELQdpGsFEY7qYzaqBjtfUc7n9vaaYcoa4thYmf6NUNQtUOHBWADV/9eZGiJTHoOYBcb56a3aOk4r8870MsgHtGJRxQxHb9u0deMhZ3G4fJNRX7yvkaytyzUehIoQ0vELgdOunFoeoVK3Sx6bQZ6EEYoqAYQa1f2oLY9U6Y9TUmx+o1Tq6mI21xgaM+W8e/kyjDZmYVkAfECD01lNqvmu/1cIhXkBPBPU5KTos4QyryXhF0CtDks/A/A2Lh9o5KzzFvyKX/HM8b/Vahr3NgurtwAAAABJRU5ErkJggg==', 'enforcesSecureChat': False, 'previewsChat': True}":
    print(hex(x))