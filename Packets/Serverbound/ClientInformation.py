class ClientInformation:
    def create(self, bytebuf, decryptor):
        locale = bytebuf.unpack_encrypted_string(decryptor)
        view_distance = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)
        chat_mode, byte_length = bytebuf.unpack_encrypted_varint(decryptor)
        chat_colors = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)
        displayed_skin_parts = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor) #should be unsigned?
        main_hand, byte_length = bytebuf.unpack_encrypted_varint(decryptor)
        text_filtering = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)
        allow_server_listing = bytebuf.decrypt_byte(bytebuf.recv(1), decryptor)

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