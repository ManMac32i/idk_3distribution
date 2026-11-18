from src import *
import gurobipy as gp

filename = "01.txt"
foldername = "instances"
demand, capacity, demand, coordinates = get_data(1)
