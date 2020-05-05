class relation:
    def __init__(self, serviceSupporter, serviceConsumer, relationType):
        self.serviceSupporter = serviceSupporter
        self.serviceConsumer = serviceConsumer
        self.relationType = relationType

    def getRelation(self):
        return {'supporter': self.serviceSupporter, 'consumer': self.serviceConsumer, 'type': self.relationType}
