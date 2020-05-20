import json
# from .Relation import relation
# from .Service import service
# from .Server import server
import logging


class serviceTree:
    def __init__(self, name, label, customerId=0, itsmprepend="", itsmappend="") -> None:
        self.services = []
        self.relations = []

        self.name = name
        self.label = label
        self.itsmprepend = itsmprepend
        self.itsmappend = itsmappend
        self.customerId = customerId

    def getServiceNameFromLabel(self, label):
        for s in self.services:
            if s['label'] == label:
                return s['name']

        logging.critical(
            f"getServiceNameFromLabel didn't find a service matching '{label}'")
        raise Exception(
            f"getServiceNameFromLabel didn't find a service matching '{label}'")

    def getServiceLabelFromName(self, name):
        for s in self.services:
            if s['name'] == name:
                return s['label']

        logging.critical(
            f"getServiceLabelFromName didn't find a service matching '{name}'")
        raise Exception(
            f"getServiceLabelFromName didn't find a service matching '{name}'")

    def addRelation(self, provider, consumer, relationType):

        rel = {'provider': provider, 'consumer': consumer, 'type': relationType}

        self.relations.append(rel)

    def deleteRelation(self, provider, consumer, relationType=None):
        result = []

        for r in self.relations:
            logging.debug(
                f"provider is '{provider}' and consumer is '{consumer}' with the relation '{relationType}'")
            if r['provider'] != provider and r['consumer'] != consumer:
                result.append(r)
            else:
                if relationType != r['type']:
                    result.append(r)
                else:
                    pass

        self.relations = result

    def clearRelations(self):
        self.relations = []

    def loadFromJSON(self, jsonInput: json):
        """Loading a full service tree with children based on JSON input
        Primarily functions to ensure some sort of quality control

        Arguments:
            jsonInput {json} -- JSON input following schema
        """
        logging.debug(f"JSON input to loadFromJSON is: {jsonInput}")
        if type(jsonInput) == str:
            jsonInput = json.loads(jsonInput.replace('\'', '\"'))

        self.name = jsonInput['name']
        self.label = jsonInput['label']
        self.customerId = jsonInput['customerId']

        try:
            self.itsmprepend = jsonInput['itsmprepend']
            self.itsmappend = jsonInput['itsmappend']
        except:
            pass

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
        Primarily functions to ensure some sort of quality control

        Returns:
            json -- Full JSON representation of the service tree
        """
        root = {}
        root['name'] = self.name
        root['label'] = self.label
        root['customerId'] = self.customerId
        root['itsmprepend'] = self.itsmprepend
        root['itsmappend'] = self.itsmappend

        root['services'] = self.services

        logging.debug('Added services')

        root['relations'] = self.relations

        logging.debug('Added relations')

        return root
