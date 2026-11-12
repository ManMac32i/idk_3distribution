import json
import numpy as np

class GetData():
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.lines = file.readlines()
        for l in range(len(self.lines)): 
            self.lines[l] = self.lines[l].replace("\n", "")

        self.dimension = int(self.lines[0].replace("DIMENSION : ","")) # dimension of the truck   
        self.capacity = int(self.lines[1].replace("CAPACITY : ","")) # capacity of the truck 

        self.demand = [] # demand of the problem
        self.coordinates = [] # coordinates of the problem

        for line in range(3 ,len(self.lines)): # get the coordinates (skip the third useless line)
            if self.lines[line] == "DEMAND_SECTION ": # when it finds the demands section stops the loop
                for demand in range(line + 1, len(self.lines)):
                    values = [int(x) for x in self.lines[demand].split()]
                    self.demand.append(values[1])
                break
            else: 
                values = [int(x) for x in self.lines[line].split()]
                self.coordinates.append((values[1], values[2])) # coordinates of the points, starts from 0

    def get_capacity(self):
        return self.capacity
    
    def get_dimension(self):
        return self.dimension
    
    def get_coordinates(self):
        return self.coordinates
    
    def get_demand(self):
        return self.demand
    
