
class Exchange:
    def __init__(self, name: str):
        self.name = name.upper()

    def get_name(self):
        return self.name


class ExchangeSocket:
    def __init__(self, name: str):
        self.name = name.upper()

    def get_name(self):
        return self.name
