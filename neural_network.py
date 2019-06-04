import numpy as np


class Network:

    number_of_hidden_layers = 0
    node_for_first_layer = 0
    node_for_hidden_layer = 0
    node_for_last_layer = 0
    layers = []
    weights = []

    def __init__(self, number_of_hidden_layers, node_for_first_layer, node_for_hidden_layer, node_for_last_layer,
                 weights):
        self.layers = []
        self.weights = []
        self.number_of_hidden_layers = number_of_hidden_layers
        self.node_for_layer = node_for_hidden_layer
        self.weights = weights
        self.add_layer(node_for_first_layer)
        for hidden_layer_num in range(number_of_hidden_layers):
            self.add_layer(node_for_hidden_layer)
        self.add_layer(node_for_last_layer)

    def set_first_layer(self, layer):
        self.layers[0] = layer

    def add_layer(self, size):
        self.layers.append(self.create_layer(size))

    def calculate_output(self):
        for layer_number in range(self.number_of_hidden_layers + 1):
            for node_number in range(len(self.layers[layer_number])):
                self.layers[layer_number][node_number] = self.sigmoid_bipolar(self.layers[layer_number][node_number])
                for edge_number in range(len(self.layers[layer_number + 1])):
                    if node_number == 0:
                        self.layers[layer_number + 1][edge_number] = 0
                    self.layers[layer_number + 1][edge_number] += self.layers[layer_number][node_number] * self.weights[
                        layer_number][node_number][edge_number]
        output = []
        for node in self.layers[-1]:
            output.append(node)
        return output

    @staticmethod
    def create_layer(size):
        layer = []
        for node in range(size):
            layer.append(0)
        return layer

    @staticmethod
    def sigmoid(value):
        return 1 / (1 + np.exp(-value))

    @staticmethod
    def sigmoid_bipolar(value):
        return (1 - np.exp(-value)) / (1 + np.exp(-value))

    @staticmethod
    def tangent_hyperbolic(value):
        return (np.exp(value) - np.exp(-value)) / (np.exp(value) + np.exp(-value))
