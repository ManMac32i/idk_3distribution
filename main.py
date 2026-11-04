import os
from  data_getter import *

filename = "01.txt"
foldername = "instances"
inst = GetData(os.path.join(".", foldername, filename))
data = GetData.instances_data(inst)