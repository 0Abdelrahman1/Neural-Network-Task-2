import copy
import random

import numpy as np
FEATURES = 5
CLASSES = 3
import math
import numpy as np


def weight_initialize(hidden_layers):
    # NOTE!!!! FISRT index represents the number of {{ input layer features}}
    # hidden_layers = np.array([4,2,3]) # first index isn't one of the hidden layers
    hidden_layers = np.append(np.array([FEATURES]), hidden_layers)
    weights = []
    for i in range(len(hidden_layers) - 1):
        x = np.random.uniform(-1.0, 1.0, (hidden_layers[i + 1], hidden_layers[i]))
        # x = np.random.rand(hidden_layers[i+1], hidden_layers[i])

        new_column = np.ones((x.shape[0], 1))
        # Add the new column to the array
        result = np.hstack((x, new_column))
        weights.append(result)

    x = np.random.uniform(-1.0, 1.0, (CLASSES, hidden_layers[-1]))
    # x = np.random.rand(3, hidden_layers[len(hidden_layers)-1])

    new_column = np.ones((CLASSES, 1))
    result = np.hstack((x, new_column))
    weights.append(result)
    #print(weights)

    return weights


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def tangent(x):
    return (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))

def forward(input_layer, weights, bias_flag, sigmoid0_tangent1):
    number_of_layers = len(weights)
    output = []
    temp = []
    if sigmoid0_tangent1 == False:
        for layer_index in range(number_of_layers):
            if layer_index == 0:
                for perceptron in weights[layer_index]:
                    input_layers = np.append(np.array(input_layer), 1)
                    temp.append(sigmoid(np.dot(input_layers, perceptron)))
                temp.append(bias_flag)
                output.append(temp)
            else:
                i = 1
                temp = []
                for perceptron in weights[layer_index]:
                    x = np.dot(output[layer_index - 1], perceptron)
                    y = sigmoid(x)
                    temp.append(y)
                    i = i + 1
                temp.append(bias_flag)
                output.append(temp)
        return output
    else:
        for layer_index in range(number_of_layers):
            if layer_index == 0:
                for perceptron in weights[layer_index]:
                    input_layers = np.append(np.array(input_layer), 1)
                    temp.append(tangent(np.dot(input_layers, perceptron)))
                temp.append(bias_flag)
                output.append(temp)
            else:
                i = 1
                temp = []
                for perceptron in weights[layer_index]:
                    x = np.dot(output[layer_index - 1], perceptron)
                    y = tangent(x)
                    temp.append(y)
                    i = i + 1
                temp.append(bias_flag)
                output.append(temp)
        return output


def backward(expected, activation_outputs, weights, sigmoid0_tangent1):
    _weights = weights.copy()
    t = [0] * (CLASSES + 1)
    t[expected] = 1
    signal_errors = activation_outputs.copy()
    signal_errors[-1] = ((sigmoid0_tangent1 + np.array(activation_outputs[-1])) * (1 - np.array(activation_outputs[-1])) * (np.array(t) - np.array(activation_outputs[-1]))).tolist()
    layers = len(activation_outputs)
    for i in range(layers - 2, -1, -1):
        ii = i + 1
        _weights[ii] = _weights[ii].tolist()
        _weights[ii].append([0] * len(_weights[ii][0]))
        signal_errors[i] = ((sigmoid0_tangent1 + np.array(activation_outputs[i])) * (1 - np.array(activation_outputs[i])) * np.array(np.dot(signal_errors[ii], _weights[ii]))).tolist()
    return signal_errors


def weights_update(input_layer, activation_outputs, signal_errors, weights, eta):

    #input_layer = [1, 0, 1]
    #activation_outputs = [[0.66818777217, 0.73105857863, 1], [0.65494270852, 0.72189235647, 0.780211323, 1]]
    #signal_errors = [[-0.039765128273060876, -0.012769354595226929, 0.0], [-0.14801230842557633, 0.055833942357178645, -0.13379189729003302, 0.0]]
    #weights = [[[0.1, 0.3, 0.5, 0.1], [0.2, 0.4, 0.6, 0.2]], [[0.7, 0.1, 0.1], [0.8, 0.3, 0.2], [0.9, 0.5, 0.3]]]
    #eta = 0.1

    input_layer = np.append(input_layer, np.array([activation_outputs[-1][-1]]))
    #input_layer.append(activation_outputs[-1][-1])

    layers = len(activation_outputs)


    for j in range(len(activation_outputs[0]) - 1):
        for k in range(len(input_layer)):
            weights[0][j][k] = weights[0][j][k] + eta * signal_errors[0][j] * input_layer[k]

    for i in range(1, layers):
        for j in range(len(activation_outputs[i]) - 1):
            for k in range(len(activation_outputs[i - 1])):
                weights[i][j][k] = weights[i][j][k] + eta * signal_errors[i][j] * activation_outputs[i - 1][k]
    #print(f"weights = {weights}")
    return weights


def mlp(x_train, y_train, hidden_layers, eta, epochs, bias_flag, sigmoid0_tangent1):
    activation_outputs = []
    number_of_rows = len(y_train)
    weights = weight_initialize(hidden_layers)   # --> should contatin the bias also if bias_flag true
    for epoch in range(epochs):
        for i in range(number_of_rows):
            activation_outputs = forward(x_train[i], weights,bias_flag,sigmoid0_tangent1)
            #print("activation_output")
            #print(activation_outputs)
            signal_error=backward(y_train[i], activation_outputs, weights, sigmoid0_tangent1)
            weights = weights_update(x_train[i], activation_outputs, signal_error, weights, eta)
    return weights


