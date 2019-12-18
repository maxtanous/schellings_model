import sys
import csv
from Graph import Graph
import math 

class Schellings_Model:
    def __init__(self,fileName, thresholdValue,numIterations, actualData):
        self.fileName = fileName
        self.thresholdValue = float(thresholdValue)
        self.numIterations = int(numIterations)
        self.Graph = Graph(thresholdValue)
        self.actualData = {}

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
            normalizedRate = educationRate/numCountys
            currCountyRate = self.actualData.get(county)
            klDivergance += (normalizedRate * math.log(normalizedRate/currCountyRate))
        print("Total KL Divergance: ", klDivergance)
        return klDivergance

    def run(self):
        self.readFile()
        i = 0
        while i < self.numIterations:
            self.Graph.update()
            self.Graph.plot()
            i += 1
        #self.klDivergance()
        self.writeToCsv()


fileName = sys.argv[1]
thresholdValue = sys.argv[2]
numIterations = sys.argv[3]

actualData = {} # compute data.

schelling = Schellings_Model(fileName,thresholdValue,numIterations, actualData)
schelling.run()
