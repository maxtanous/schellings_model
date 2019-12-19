
class Node:
    def __init__(self, index, countyName, population, educatedPop, xcoordinate,ycoordinate):
        #index of the node, used for lists
        self.index = int(index)
        self.countyName = countyName
        #number of college educated people in the county
        self.educatedPop = int(educatedPop)
        #population of the county
        self.population = int(population)
        #the percent of educated people in the county
        self.educationRate = float(self.educatedPop/self.population)
        #education value, a huerisitc value computing the percieved education level of the county
        self.educationValue = 0
        #the coordinates of the most populus city in the county
        self.coordinates = (float(xcoordinate),float(ycoordinate))

    def updateEV(self, value):
        self.educationValue = value

    def updatePop(self,delta_educated_pop):
        #when the population is updated we also must recompute the education rate
        self.educatedPop +=  delta_educated_pop
        self.population += delta_educated_pop
        self.educationRate = self.educatedPop/self.population
