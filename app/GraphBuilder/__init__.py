from graphviz import Digraph
import json


class graphBuilder:
    def __init__(self) -> None:
        pass

    def addService(self, id, name, type) -> None:
        pass


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


class relation:
    def __init__(self, serviceSupporter, serviceConsumer, relationType):
        self.serviceSupporter = serviceSupporter
        self.serviceConsumer = serviceConsumer
        self.relationType = relationType

    def getRelation(self):
        return {'supporter': self.serviceSupporter.name, 'consumer': self.serviceConsumer.name, 'type': self.relationType}


class server:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getServer(self):
        return {'id': self.id, 'name': self.name}


class service:
    def __init__(self, name, label, serviceType) -> None:
        """Service Object holding list of servers included

        Arguments:
            name {string} -- Internal name, can be a numeric id
            label {string} -- External label, will be shown on graph
            serviceType {string} -- Not in use yet, but will be e.g. SaaS, A/P cluster, A/A farm etc
        """
        self.name = name
        self.label = label
        self.type = serviceType
        self.servers = []

    def addServer(self, id, name) -> None:
        """Adds a server to the specification

        Arguments:
            id {string} -- Internal id, can be a numeric id
            name {string} -- External label, will be shown on graph
        """
        self.servers.append({'id': id, 'name': name})

    def clearServers(self) -> None:
        """Clears the serverlist - e.g. for resetting before re-adding servers
        """
        self.servers = []

    def getService(self):
        """Returns the JSON representation of the service, including the server list

        Returns:
            json -- The full representation of the service
        """
        r = {}
        r['name'] = self.name
        r['label'] = self.label
        r['type'] = self.type
        r['servers'] = self.servers

        return r
