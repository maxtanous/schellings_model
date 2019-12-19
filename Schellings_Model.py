import sys
import csv
from Graph import Graph
import math 

class Schellings_Model:
    def __init__(self,fileName, numIterations, actualData):
        self.fileName = fileName
        self.numIterations = int(numIterations)
        self.Graph = Graph()
        self.actualData = actualData

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

    def writeToCsv(self):
        with open('final-iter.csv', mode='w') as file:
            csvwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['CountyName', 'EducationRate', 'Population'])
            for node in self.Graph.nodes: 
                csvwriter.writerow([node.cityName, str(node.educationRate), str(node.population)])
    
    
    def klDivergance(self):
        klDivergance = 0
        numCountys = len(self.Graph.nodes)
        for node in self.Graph.nodes:
            county = node.cityName
            educationRate = node.educationRate
            normalizedRate = (educationRate * node.population)/numCountys
            currCountyRate = self.actualData[county]
            klDivergance += (normalizedRate * math.log(normalizedRate/currCountyRate))
        print("Total KL Divergance: ", klDivergance)
        

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
        self.klDivergance()
        self.writeToCsv()


fileName = sys.argv[1]
numIterations = sys.argv[3]


actualData = {'Androscoggin': 14.8, 'Aroostook': 12.9, 'Cumberland': 28.2, 'Franklin': 16.7, 'Hancock': 19.2,
 'Kennebec': 16.4, 'Knox': 19.7, 'Lincoln': 18.7, 'Oxford': 12.2, 'Penobscot': 16.7, 'Piscataquis': 12.4,
 'Sagadahoc': 22, 'Somerset': 11.8, 'Waldo': 19.4, 'York': 20.6, 'Washington': 13.7} # compute data.

schelling = Schellings_Model(fileName,thresholdValue,numIterations, actualData)
schelling.run()
