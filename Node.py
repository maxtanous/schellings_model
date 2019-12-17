
class Node:
    def __init__(self, index, cityName, population, educatedPop, xcoordinate,ycoordinate):
        self.index = int(index)
        self.cityName = cityName
        self.educatedPop = int(educatedPop)
        self.population = int(population)
        self.educationRate = float(self.educatedPop/self.population)
        self.educationValue = 0
        self.coordinates = (float(xcoordinate),float(ycoordinate))

    def updateEV(self, value):
        self.educationValue = value

    def updatePop(self,delta_educated_pop):
        self.educatedPop +=  delta_educated_pop
        self.population += delta_educated_pop
        self.educationRate = self.educatedPop/self.population
