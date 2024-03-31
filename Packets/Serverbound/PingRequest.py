class PingRequest:
    def create(self, remaining_packet_length, socket):
        time = socket.recv(8)

        self.time = time

        return self

    def get(self, item):
        return self.__dict__[item]