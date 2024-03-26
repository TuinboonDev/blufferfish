class AcknowledgeFinishConfiguration:
    def create(self, socket):
        return self

    def get(self, item):
        return self.__dict__[item]