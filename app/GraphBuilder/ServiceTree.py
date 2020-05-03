import json
#from app.GraphBuilder import relation
from .Relation import relation
from .Service import service
from .Server import server


class serviceTree:
    def __init__(self, name, label, customerId) -> None:
        self.services = []
        self.relations = []

        self.name = name
        self.label = label
        self.customerId = customerId

    def getServiceFromName(self, name):
        for s in self.services:
            if s.name == name:
                return s

        raise Exception(
            f"getServiceFromName didn't find a service matching '{name}'")

    def loadFromJSON(self, jsonInput: json):
        self.name = jsonInput['name']
        self.label = jsonInput['label']
        self.customerId = jsonInput['customerId']

        print('core loaded')
        self.services = []

        for s in jsonInput['services']:
            svc = service(s['name'], s['label'], s['type'])
            if len(s['servers']) > 0:
                for server in s['servers']:
                    svc.addServer(server['id'], server['name'])
            self.services.append(svc)

        print('services loaded')
        self.relations = []
        for r in jsonInput['relations']:
            self.relations.append(relation(self.getServiceFromName(r['supporter']), self.getServiceFromName(r['consumer']), r['type'])
                                  )

        print('all done')

    def getServiceTreeAsJSON(self):
        """Returns a JSON representation of the service tree

        Returns:
            json -- Full JSON representation of the service tree
        """
        root = {}
        root['name'] = self.name
        root['label'] = self.label
        root['customerId'] = self.customerId

        services = []
        for s in self.services:
            services.append(s.getService())

        root['services'] = services

        relations = []
        for r in self.relations:
            relations.append(r.getRelation())

        root['relations'] = relations

        return root
