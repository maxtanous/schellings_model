import sys
import csv
from Graph import Graph

class Schellings_Model:
    def __init__(self,fileName, thresholdValue,numIterations):
        self.fileName = fileName
        self.thresholdValue = float(thresholdValue)
        self.numIterations = int(numIterations)
        self.Graph = Graph(thresholdValue)

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
            print(row)
            nodes += [row]
        self.Graph.initNodes(nodes)

    def run(self):
        self.readFile()
        i = 0
        while i < self.numIterations:
            self.Graph.update()
            self.Graph.plot()
            i += 1


fileName = sys.argv[1]
thresholdValue = sys.argv[2]
numIterations = sys.argv[3]

schelling = Schellings_Model(fileName,thresholdValue,numIterations)
schelling.run()
