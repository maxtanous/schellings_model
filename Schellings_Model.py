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
        #read in the file and initialize the counties
        self.readFile()
        i = 0
        #graph the initial graph
        self.Graph.plot("Maine Education Map (Initial Data 2000)")
        while i < self.numIterations:
            #at each iteration update the graph
            self.Graph.update()
            #plot the results after each iteration
            self.Graph.plot("Maine Education Map (Iteration: " + str(i+1) +  ", Local Influence 2x)")
            i += 1


fileName = sys.argv[1]
numIterations = sys.argv[3]

schelling = Schellings_Model(fileName,numIterations)
schelling.run()
