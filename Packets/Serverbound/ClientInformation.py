from Packets.PacketUtil import decrypt_byte, unpack_encrypted_varint

class ClientInformation:
    def create(self, remaining_packet_length, socket):
        locale_length, byte_length = unpack_encrypted_varint(socket)
        locale = ''
        for i in range(locale_length):
            locale += decrypt_byte(socket.recv(1)).decode('utf-8')
        view_distance = decrypt_byte(socket.recv(1))
        chat_mode, byte_length = unpack_encrypted_varint(socket)
        chat_colors = decrypt_byte(socket.recv(1))
        displayed_skin_parts = decrypt_byte(socket.recv(1)) #should be unsigned?
        main_hand, byte_length = unpack_encrypted_varint(socket)
        text_filtering = decrypt_byte(socket.recv(1))
        allow_server_listing = decrypt_byte(socket.recv(1))

        self.locale = locale
        self.view_distance = view_distance
        self.chat_mode = chat_mode
        self.chat_colors = chat_colors
        self.displayed_skin_parts = displayed_skin_parts
        self.main_hand = main_hand
        self.text_filtering = text_filtering
        self.allow_server_listing = allow_server_listing
        return self

    def get(self, item):
        return self.__dict__[item]