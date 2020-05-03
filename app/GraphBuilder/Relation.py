class relation:
    def __init__(self, serviceSupporter, serviceConsumer, relationType):
        self.serviceSupporter = serviceSupporter
        self.serviceConsumer = serviceConsumer
        self.relationType = relationType

    def getRelation(self):
        return {'supporter': self.serviceSupporter.name, 'consumer': self.serviceConsumer.name, 'type': self.relationType}
