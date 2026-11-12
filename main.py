import os
from data_folder import *


filename = "01.txt"
foldername = "instances"
inst = GetData(os.path.join(".", foldername, filename))
demand = GetData.get_demand()
capacity = GetData.get_capacity()
dimension = GetData.get_dimension()
coordinates = GetData.get_coordinates()