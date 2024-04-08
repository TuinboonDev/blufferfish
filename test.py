class ClientError:
    def __init__(self, message):
        print("b")
        print(f"\u001b[33m{message}")

ClientError("This is a test error")