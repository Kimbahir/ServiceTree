from .Server import server


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
        self.servers.append(server(id, name))

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
        servers = []
        for s in self.servers:
            servers.append(s.getServer())
        r['servers'] = servers

        return r
