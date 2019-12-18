import sys
import csv
from Graph import Graph

class Schellings_Model:
    def __init__(self,fileName,numIterations):
        self.fileName = fileName
        self.numIterations = int(numIterations)
        self.Graph = Graph()

    def readFile(self):
        rows = []
        # reading csv file
        with open(self.fileName, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
        nodes = []
        for row in rows:
            nodes += [row]
        self.Graph.initNodes(nodes)

    def run(self):
        self.readFile()
        i = 0
        self.Graph.plot("Maine Education Map (Initial Data 2000)")
        while i < self.numIterations:
            self.Graph.update()
            self.Graph.plot("Maine Education Map (Iteration: " + str(i+1) +  ", Local Influence 5x)")
            i += 1


fileName = sys.argv[1]
numIterations = sys.argv[3]

schelling = Schellings_Model(fileName,numIterations)
schelling.run()
