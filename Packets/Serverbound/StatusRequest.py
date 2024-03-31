class StatusRequest:
    def create(self, remaining_packet_length, socket):
        return self

    def get(self, item):
        return self.__dict__[item]