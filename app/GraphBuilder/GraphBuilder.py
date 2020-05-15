from graphviz import Digraph
from app.GraphBuilder.ServiceTree import serviceTree
import logging
import json
from io import BytesIO
import base64


class graphBuilder:
    def __init__(self, serviceTree=None) -> None:
        self.serviceTree = serviceTree

    def loadServiceTreeFromJSON(self, jsonInput):
        self.serviceTree = serviceTree('', '', '')
        self.serviceTree.loadFromJSON(jsonInput)

    def setServiceTree(self, serviceTree):
        self.serviceTree = serviceTree

    def getServiceArrayFromCSV(self, csv):
        result = []

        currentService = "absolutelynotgonnahappenever"
        tmp = {}
        for idx, record in enumerate(csv.split('\r')):
            logging.debug(record)

            row = record.replace('\n', '').split(',')
            if idx == 0 or row[0] != currentService:
                currentService = row[0]
                if idx != 0:
                    result.append(tmp)
                tmp = {
                    "name": row[0],
                    "label": row[0],
                    "type": "none",
                    "servers": []
                }

            srv = {"id": row[1], "name": row[2]}
            tmp["servers"].append(srv)

        result.append(tmp)

        return result

    def drawGraphForWeb(self, format='pdf'):
        """Draws the actual graph, based on the current service tree.

        Keyword Arguments:
            format {str} -- graphviz output format (default: {pdf})
        """
        g = Digraph(comment=self.serviceTree.name)
        g.attr(rankdir='TB')
        g.attr(shape='circle')

        for service in self.serviceTree.services:
            label = self.getHtmlTable(service)

            g.node(service['name'], shape='none', label=label,
                   URL="https://github.com/Kimbahir/ServiceTree")

        for relation in self.serviceTree.relations:
            if relation['type'] == "vital":
                g.edge(relation['supporter'],
                       relation['consumer'], penwidth="3.0", color="blue")
            else:
                g.edge(relation['supporter'],
                       relation['consumer'])

        logging.debug(g.source)

        g.format = format

        b = BytesIO()
        b.write(g.pipe())
        logging.debug('Data written')
        return b

    def drawGraph(self, filename=None, view=True):
        """Draws the actual graph, based on the current service tree.

        Keyword Arguments:
            filename {str} -- Placement of output (default: {None})
            view {bool} -- Is output to be presented to user? (default: {True})
        """
        g = Digraph(comment=self.serviceTree.name)
        g.attr(rankdir='TB')
        g.attr(shape='circle')

        for service in self.serviceTree.services:
            label = self.getHtmlTable(service)

            g.node(service['name'], shape='none', label=label,
                   URL="https://github.com/Kimbahir/ServiceTree")

        for relation in self.serviceTree.relations:
            if relation['type'] == "vital":
                g.edge(relation['supporter'],
                       relation['consumer'], penwidth="3.0", color="blue")
            else:
                g.edge(relation['supporter'],
                       relation['consumer'])

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
        #service = json.loads(service)
        if service['type'] == "farm":
            headingfillcolor = "blue4"
            cellfillcolor = "cadetblue1"
            headingtextcolor = "white"
            celltextcolor = "black"
        elif service['type'] == "aacluster":
            headingfillcolor = "blue"
            cellfillcolor = "azure2"
            headingtextcolor = "white"
            celltextcolor = "black"
        elif service['type'] == "apcluster":
            headingfillcolor = "dodgerblue1"
            cellfillcolor = "azure"
            headingtextcolor = "white"
            celltextcolor = "black"
        else:
            headingfillcolor = "grey"
            headingtextcolor = "white"
            celltextcolor = "black"
            cellfillcolor = "white"

        logging.debug(f'service is {service}')
        label = '<<table border="0" cellspacing="0">'
        label += f'<tr><td port="port0" border="1" bgcolor="{headingfillcolor}"><font color="{headingtextcolor}">{service["label"]}</font></td></tr>'

        for idx, server in enumerate(service['servers'], start=1):
            server_name = "&nbsp;"
            if server["name"] != "":
                server_name = server["name"]
            label += f'<tr><td port="port{idx}" border="1" bgcolor="{cellfillcolor}"><font color="{celltextcolor}">{server_name}</font></td></tr>'

        label += '</table>>'

        return label
