from Node import Node
import math
import numpy as np
from scipy import stats
import statistics
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors

class Graph:
    def __init__(self):
        self.localInfluence = 5
        #an indexed set of all nodes in graph
        self.nodes = []
        self.leavingMaineNode = []
        #a 2-D array of neighbors. At the index of a node, will be a list of all its neighbors indexes
        self.neighbors = []

    def initNodes(self,nodes):
        for node in nodes:
            n = Node(*node)
            self.nodes += [n]
        for node in self.nodes:
            self.neighbors += [self.getClosetCities(node)]
        self.leavingMaineNode = Node(16, "Leaving Maine", 1, 1, 46.44,-70.5)

    def getClosetCities(self,node):
        distances = [self.getDistance(node,nodeTwo) for nodeTwo in  self.nodes]
        distances = np.array(distances)
        neighbors = distances.argsort()[:5]
        return neighbors

    def update(self):
        self.updateEducationValues()
        self.updatePopulations()

    def updatePopulations(self):
        for node in self.nodes:
            percentLeaving = self.getPercentLeaving(node)
            numPeopleLeaving = int(node.educatedPop * percentLeaving)
            threshold = percentLeaving + node.educationValue
            newCityIndex = self.getNewCity(node,threshold)
            if newCityIndex == -1:
                node.updatePop(-numPeopleLeaving)
                self.leavingMaineNode.updatePop(numPeopleLeaving)
            else:
                node.updatePop(-numPeopleLeaving)
                self.nodes[newCityIndex].updatePop(numPeopleLeaving)

    def getPercentLeaving(self,node):
        evs = [node.educationValue for node in self.nodes]
        std = np.std(evs)
        mean = statistics.mean(evs)
        z_score = (node.educationValue-mean)/std
        p_value = stats.norm.sf(abs(z_score))
        delta_p = p_value - node.educationRate
        if (delta_p < 0):
            return abs(delta_p)
        else:
            return 0

    def getNewCity(self,node,threshold):
        bestNeighbor = -1
        bestEducationValue = 0
        distances = [self.getDistance(node,nodeTwo) for nodeTwo in  self.nodes]
        distances = np.array(distances)
        neighborIndicis = distances.argsort()
        neighborIndicis = list(neighborIndicis)
        for neighborIndex in neighborIndicis:
            neighbor = self.nodes[neighborIndex]
            educationValue = neighbor.educationValue
            if educationValue > threshold:
                return neighborIndex
        return -1

    def getDistance(self,node1,node2):
        x1,y1 = node1.coordinates
        x2,y2 = node2.coordinates
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return distance

    def getNeighbors(self,node):
        neighbors = []
        for neighborIndex in self.neighbors[node.index]:
            neighbor = self.nodes[neighborIndex]
            neighbors += [neighbor]
        return neighbors

    def updateEducationValues(self):
        for node in self.nodes:
            ev = self.getEducationValue(node)
            node.updateEV(ev)

    def getEducationValue(self,node):
        sumPopulations = node.population
        numEducatedPeople = []
        for neighbor in self.getNeighbors(node):
            sumPopulations += neighbor.population
            numEducatedPeople += [neighbor.educatedPop]
        educationValue = (self.localInfluence * node.educatedPop + sum(numEducatedPeople))/sumPopulations
        return educationValue

    def plot(self,title):
        self.nodes += [self.leavingMaineNode]
        G_nx = nx.DiGraph()
        for node in self.nodes:
            G_nx.add_node(node.index)

        nodeIndex = 0
        for neighborSet in self.neighbors:
            for neighbor in neighborSet:
                G_nx.add_edge(nodeIndex, neighbor)
            nodeIndex += 1
        cmap = plt.cm.Blues
        norm = matplotlib.colors.Normalize(vmin=0, vmax=.6)
        pos = {}
        sizes = []
        labels = {}
        colors = []
        for node in self.nodes:
            pos[node.index] = [node.coordinates[0],node.coordinates[1]]
            sizes += [math.log1p(node.population)*155]
            if node.index == 16:
                labels[node.index] = node.countyName + '\n ' + str(node.population)
            else:
                labels[node.index] = node.countyName + '\n ' + str(round(node.educationRate* 100,2) ) + '%'
            colors += [cmap(norm(node.educationRate))]

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        plt.colorbar(sm, label="% Bachelor Degree or Higher")
        nx.draw_networkx_nodes(G_nx, pos, node_size=sizes,with_labels=True, node_color = colors)
        # edges
        nx.draw_networkx_edges(G_nx, pos, width=1)
        nx.draw_networkx_labels(G_nx, pos, font_size=6, labels=labels,font_family='sans-serif')
        plt.title(title)
        plt.show()
        self.nodes.pop()
