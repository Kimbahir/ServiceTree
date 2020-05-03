class server:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getServer(self):
        return {'id': self.id, 'name': self.name}
