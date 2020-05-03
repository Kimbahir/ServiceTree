from graphviz import Digraph
from .Server import server
from .Relation import relation
from .ServiceTree import serviceTree
from .Service import service
import logging
import json


class graphBuilder:
    def __init__(self, serviceTree=None) -> None:
        self.serviceTree = serviceTree

    def loadServiceTreeFromJSON(self, jsonInput):
        self.serviceTree = serviceTree('', '', '')
        self.serviceTree.loadFromJSON(jsonInput)

    def setServiceTree(self, serviceTree):
        self.serviceTree = serviceTree

    def drawGraph(self, filename=None, view=True):
        g = Digraph(comment=self.serviceTree.name)
        g.attr(rankdir='TB')
        g.attr(shape='circle')

        #g.node('user', label='User')

        for service in self.serviceTree.services:
            label = self.getHtmlTable(service)
            print(label)
            g.node(service.name, shape='none', label=label,
                   URL="http://morticia.dk")

        for relation in self.serviceTree.relations:
            if relation.relationType == "vital":
                g.edge(relation.serviceSupporter.name,
                       relation.serviceConsumer.name, penwidth="2.0", color="red")
            else:
                g.edge(relation.serviceSupporter.name,
                       relation.serviceConsumer.name)
            # relation.serviceConsumer.

        logging.debug(g.source)

        g.format = 'svg'

        if filename == None:
            g.view()
        else:
            g.render(filename, view=view)

    def getHtmlTable(self, service):
        """Returns the HTML form (compliant with graphviz) of a label

        Arguments:
            service {service} -- The Service containing the servers array

        Returns:
            str -- HTML representation of the label
        """
        if service.type == "farm":
            headingfillcolor = "blue4"
            cellfillcolor = "cadetblue1"
            headingtextcolor = "white"
            celltextcolor = "black"
        elif service.type == "aacluster":
            headingfillcolor = "blue"
            cellfillcolor = "azure2"
            headingtextcolor = "white"
            celltextcolor = "black"
        elif service.type == "apcluster":
            headingfillcolor = "dodgerblue1"
            cellfillcolor = "azure"
            headingtextcolor = "white"
            celltextcolor = "black"
        else:
            headingfillcolor = "grey"
            headingtextcolor = "black"
            celltextcolor = "black"
            cellfillcolor = "white"

        label = '<<table border="0" cellspacing="0">'
        label += f'<tr><td port="port0" border="1" bgcolor="{headingfillcolor}"><font color="{headingtextcolor}">{service.label}</font></td></tr>'

        for idx, server in enumerate(service.servers, start=1):
            label += f'<tr><td port="port{idx}" border="1" bgcolor="{cellfillcolor}"><font color="{celltextcolor}">{server.name}</font></td></tr>'

        label += '</table>>'

        return label
