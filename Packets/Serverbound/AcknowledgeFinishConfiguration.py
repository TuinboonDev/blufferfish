class AcknowledgeFinishConfiguration:
    def create(self, bytebuf, decryptor):
        return self

    def get(self, item):
        return self.__dict__[item]