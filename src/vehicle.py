from .helpers.configuration import *

class Vehicle:
    def __init__(self, capacity, v_type):
        self.capacity = capacity
        self.v_type = v_type
        self.emisions = emisions[v_type]