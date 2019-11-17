import pandas as pd

class Building(object):
    def __init__(self,name):
        self.name = name
        self.roads = {}
        
    def connect(self,other,weight,option="two-way"):
        self.roads[other] = weight
        if option == "two-way":
            other.roads[self] = weight
    def __str__(self):
        res = self.name + "'s road to\n"
        for key,value in self.roads.items():
            res += key.name + ": " + str(value) + " meter\n"
        return res

class Area(object):
    def __init__(self):
        self.graph = {}
        self.deg = {}
    def __str__(self):
        res = "The area has the following building:\n"
        for value in self.graph.values():
            res += value.name + ", "
        res += "\n"
        return res
    def newBuilding(self):
        print(self)
        name = input("Building name: ")
        building = Building(name)
        no = input("Building(s) that is(are) adjacent to this building: ")
        if no:
            dist = input("The respective distance: ")
            dist = [int(measure) for measure in dist.split(",")]
            adjacent = no.split(", ")
            try:
                for it in range(len(dist)):
                    building.connect(self.graph[adjacent[it]],dist[it])
            except:
                print("The building has not yet built.\n")
                return
        self.graph[name] = building
    def importBuilding(self,bName):
        building = Building(bName)
        self.graph[bName] = building
    def degree(self):
        for x in self.graph.values():
            for y in self.graph.values():
                self.deg[(x,y)] = 1000
                self.deg[(y,x)] = 1000

df = pd.read_csv("building.csv")
condf = pd.read_csv("connection.csv")

vals = [val for val in df["entrance_name"].values]
south = Area()
for val in vals:
    south.importBuilding(val)

firsts = [val for val in condf["building_one"].values]
seconds = [val for val in condf["building_two"].values]
weights = [val for val in condf["distance"].values]
for it in range(len(firsts)):
    south.graph[firsts[it]].connect(south.graph[seconds[it]],weights[it])