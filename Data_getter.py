import json
import numpy as np


class GetData():
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.lines = file.readlines()
        for l in range(len(self.lines)): 
            self.lines[l] = self.lines[l].replace("\n", "")

        self.capacity = 0 # capacity of the truck
        self.dimension = 0 # dimension of the truck 
        self.coordinates = [] # coordinates of the problem

    def instances_data(self):
        self.dimension = int(self.lines[0].replace("DIMENSION : ","")) # get the dimension 
        self.capacity = int(self.lines[1].replace("CAPACITY : ","")) # get the capacity
        for line in range(3 ,len(self.lines)): # get the coordinates (skip the third useless line)
            if self.lines[line] == "DEMAND_SECTION ":
                break
            else: 
                values = [int(x) for x in self.lines[line].split()]
                self.coordinates.append((values[1], values[2])) # coordinates of the points, starts from 0


        return self.capacity, self.dimension, self.coordinates 
    
    