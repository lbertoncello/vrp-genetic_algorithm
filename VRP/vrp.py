import numpy as np

class VRP():
    def __init__(self):
        self.__dimension = -1
        self.__capacity = -1
        self.__current_node_index = 0
        self.__current_demand_index = 0
        self.number_of_trucks = -1

    def set_dimension(self, dimension):
        self.__dimension = dimension
        self.nodes = np.zeros((dimension, 2))
        self.demands = np.zeros((dimension, 1))

    def set_capacity(self, capacity):
        self.__capacity = capacity

    def get_capacity(self):
        return self.__capacity
    
    def get_dimension(self):
        return self.__dimension

    def append_node(self, node):
        self.nodes[self.__current_node_index] = node
        self.__current_node_index += 1

    def append_demand(self, demand):
        self.demands[self.__current_demand_index] = demand
        self.__current_demand_index += 1