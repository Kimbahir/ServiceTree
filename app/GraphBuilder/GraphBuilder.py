from graphviz import Digraph
from app.GraphBuilder.ServiceTree import serviceTree
import logging
import json
from io import BytesIO
import base64
from datetime import datetime


class graphBuilder:
    def __init__(self, serviceTree=None) -> None:
        self.serviceTree = serviceTree

    def loadServiceTreeFromJSON(self, jsonInput):
        self.serviceTree = serviceTree('', '', '')
        self.serviceTree.loadFromJSON(jsonInput)

    def setServiceTree(self, serviceTree):
        self.serviceTree = serviceTree

    def setServiceArrayFromCSV(self, csv):
        self.serviceTree.services = self.getServiceArrayFromCSV(csv)

    def getServiceArrayFromCSV(self, csv):
        """Generates a new service array from a CSV input. CSV can have either 1, 3 or 4 columns

        Arguments:
            csv {str} -- 1, 3 or 4 columns, for ServiceName, +Server ID, +Server Name, +ServiceType

        Returns:
            array -- Returns an array of dicts containing services with associated servers
        """
        result = []

        currentService = "absolutelynotgonnahappenever"
        tmp = {}

        for idx, record in enumerate(csv.split('\r')):

            row = record.replace('\n', '').replace('\r', '').split(',')

            if row[0] == "":
                continue

            if idx == 0 or row[0] != currentService:
                currentService = row[0]
                if idx != 0:
                    result.append(tmp)
                if len(row) == 4:
                    service_type = row[3]
                else:
                    service_type = "none"
                tmp = {
                    "name": row[0],
                    "label": row[0],
                    "type": service_type,
                    "servers": []
                }

            if len(row) >= 3 and (row[1] != "" and row[2] != ""):
                srv = {"id": row[1], "name": row[2]}
                tmp["servers"].append(srv)

        result.append(tmp)

        return result

    def drawGraphObject(self, base_url=""):
        g = Digraph(comment=self.serviceTree.name)
        now = datetime.now().strftime("%d-%m-%Y %H:%M")
        g.attr(
            'graph', label=f'[DEMO] {self.serviceTree.label} - created on {now}')
        g.attr('graph', fontname='verdana', fontsize='10')
        g.attr('node', fontname='verdana', fontsize='12')
        g.attr(rankdir='TB')
        g.attr(shape='circle')

        for service in self.serviceTree.services:
            label = self.getHtmlTable(service)

            g.node(service['name'], shape='none', label=label,
                   URL=f"{base_url}/servicedetails/{service['name']}")

        for relation in self.serviceTree.relations:
            if relation['type'] == "vital":
                g.edge(relation['provider'],
                       relation['consumer'], penwidth="3.0", color="blue")
            else:
                g.edge(relation['provider'],
                       relation['consumer'])

        return g

    def drawServiceDetails(self, service_name):
        g = Digraph(comment=self.serviceTree.name)
        now = datetime.now().strftime("%d-%m-%Y %H:%M")

        service_label = self.serviceTree.getServiceLabelFromName(service_name)

        g.attr(
            'graph', label=f'[DEMO] {self.serviceTree.label} - Service: {service_label} - created on {now}')
        g.attr('graph', fontname='verdana', fontsize='10')
        g.attr('node', fontname='verdana', fontsize='12')
        # g.attr(rankdir='TB')
        g.attr(shape='circle')

        service = self.serviceTree.services['service_name']

        for server in service['servers']:

            label = '<<table border="0" cellspacing="0">'
            label += f'<tr><td port="port0" border="1" bgcolor="white"><font color="black">{self.htmlEscape(server["name"])}</font></td></tr>'
            label += '</table>>'

            g.node(service['name'], shape='none', label=label,
                   URL=f"{self.serviceTree.itsmprepend}{server['id']}{self.serviceTree.itsmappend}")

        return g

    def drawGraphForWeb(self, format='pdf', base_url=""):
        """Draws the actual graph, based on the current service tree.

        Keyword Arguments:
            format {str} -- graphviz output format (default: {pdf})
        """

        g = self.drawGraphObject(base_url)

        logging.debug(g.source)

        g.format = format

        b = BytesIO()
        b.write(g.pipe())
        logging.debug('Data written')
        return b

    def drawSVGGraph(self, base_url=""):
        """Draws the actual graph, based on the current service tree.

        Returns:
            str -- Returns the SVG representation

        """
        g = self.drawGraphObject(base_url)

        logging.debug(g.source)

        result = g.pipe(format='svg').decode('utf-8')

        return result

    def drawSVGDetailGraph(self, service_name):
        """Draws the actual graph, based on the current service tree.

        Returns:
            str -- Returns the SVG representation

        """
        g = self.drawServiceDetails(service_name)

        logging.debug(g.source)

        result = g.pipe(format='svg').decode('utf-8')

        return result

    def drawGraph(self, filename=None, view=True):
        """Draws the actual graph, based on the current service tree.

        Keyword Arguments:
            filename {str} -- Placement of output (default: {None})
            view {bool} -- Is output to be presented to user? (default: {True})
        """
        g = self.drawGraphObject()

        logging.debug(g.source)

        g.format = 'svg'

        if filename == None:
            g.view()
        else:
            g.render(filename, view=view)

    def htmlEscape(self, text):
        """Escapes for simple HTML tags as Graphviz is vulnerable

        Arguments:
            text {str} -- strings to be html escaped

        Returns:
            str -- escaped html
        """
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;"
        }

        return "".join(html_escape_table.get(c, c) for c in text)

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
        label += f'<tr><td port="port0" border="1" bgcolor="{headingfillcolor}"><font color="{headingtextcolor}">{self.htmlEscape(service["label"])}</font></td></tr>'

        for idx, server in enumerate(service['servers'], start=1):
            server_name = "&nbsp;"
            if server["name"] != "":
                server_name = server["name"]
            label += f'<tr><td port="port{idx}" border="1" bgcolor="{cellfillcolor}"><font color="{celltextcolor}">{self.htmlEscape(server_name)}</font></td></tr>'

        label += '</table>>'

        return label
