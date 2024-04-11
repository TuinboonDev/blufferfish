class AnnotationException(Exception):
    __module__ = Exception.__module__

class ClientError(Exception):
    def __init__(self, message):
        #TODO: Change to red color
        print(f"\u001b[33m{message}\033[0m")