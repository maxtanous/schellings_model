from Node import Node
import math
import numpy as np
from scipy import stats
import statistics

class Graph:
    def __init__(self,thresholdValue):
        self.localInfluence = 10
        self.thresholdValue = float(thresholdValue)
        #an indexed set of all nodes in graph
        self.nodes = []
        #a 2-D array of neighbors. At the index of a node, will be a list of all its neighbors indexes
        self.neighbors = []

    def plot(self):
        #Plot our graph
        print("")

    def initNodes(self,nodes):
        for node in nodes:
            n = Node(*node)
            self.nodes += [n]
        for node in self.nodes:
            self.neighbors += [self.getClosetCities(node)]

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
            print()
            print("county: ", node.cityName)
            educationValue = node.educationValue
            print("educationValue: ", educationValue)
            percentLeaving = self.getPercentLeaving(educationValue)
            print("percentLeaving: ", percentLeaving)
            numPeopleLeaving = int(node.educatedPop * percentLeaving)
            newCityIndex = self.getNewCity(node)
            print("new city: ", self.nodes[newCityIndex].cityName)
            node.updatePop(-numPeopleLeaving)
            self.nodes[newCityIndex].updatePop(numPeopleLeaving)

    def getPercentLeaving(self,educationValue):
        if educationValue < self.thresholdValue:
            evs = [node.educationValue for node in self.nodes]
            std = np.std(evs)
            mean = statistics.mean(evs)
            z_score = (educationValue-mean)/std
            p_value = stats.norm.sf(abs(z_score))
            delta_p = p_value - educationValue
            if (delta_p < 0):
                return abs(delta_p)
            else:
                return 0
        else:
            return 0

    def getNewCity(self,node):
        bestNeighbor = -1
        bestEducationValue = 0
        distances = [self.getDistance(node,nodeTwo) for nodeTwo in  self.nodes]
        distances = np.array(distances)
        neighborIndicis = distances.argsort()
        neighborIndicis = list(neighborIndicis)
        for neighborIndex in neighborIndicis:
            neighbor = self.nodes[neighborIndex]
            educationValue = neighbor.educationValue
            if educationValue > self.thresholdValue:
                return neighborIndex

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
