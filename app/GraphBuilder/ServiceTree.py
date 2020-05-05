import json
from .Relation import relation
from .Service import service
from .Server import server
import logging


class serviceTree:
    def __init__(self, name, label, customerId=0) -> None:
        self.services = []
        self.relations = []

        self.name = name
        self.label = label
        self.customerId = customerId

    def getServiceFromName(self, name):
        for s in self.services:
            if s.name == name:
                return s

        logging.critical(
            f"getServiceFromName didn't find a service matching '{name}'")
        raise Exception(
            f"getServiceFromName didn't find a service matching '{name}'")

    def addRelation(self, provider, consumer, relationType):

        rel = {'supporter': provider, 'consumer': consumer, 'type': relationType}

        self.relations.append(rel)

    def loadFromJSON(self, jsonInput: json):
        """Loading a full service tree with children based on JSON input

        Arguments:
            jsonInput {json} -- JSON input following schema
        """
        logging.debug(f"JSON input to loadFromJSON is: {jsonInput}")
        if type(jsonInput) == str:
            jsonInput = json.loads(jsonInput.replace('\'', '\"'))

        self.name = jsonInput['name']
        self.label = jsonInput['label']
        self.customerId = jsonInput['customerId']

        logging.debug('Load from JSON: Core completed')
        self.services = jsonInput['services']
        for s in self.services:
            if s['name'] == '':
                s['name'] = 'n/a'
                s['label'] = 'n/a'

        logging.debug('Load from JSON: Services completed')

        self.relations = jsonInput['relations']

        logging.debug('Load from JSON: Relations completed')
        logging.info('Load from JSON: Loaded')

    def getServiceTreeAsJSON(self):
        """Returns a JSON representation of the service tree

        Returns:
            json -- Full JSON representation of the service tree
        """
        root = {}
        root['name'] = self.name
        root['label'] = self.label
        root['customerId'] = self.customerId

        services = self.services

        root['services'] = services

        logging.debug('Added services')

        relations = self.relations

        root['relations'] = relations

#        root['relations'] = self.relations
        logging.debug('Added relations')

        return root
