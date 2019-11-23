#!/bin/python

# Author: Yanzhao Wu

import matplotlib.pyplot as plt
import numpy as np

# LRBench modules
from LRBench.lr.LR import LR

class LearningRate:
    
    def __init__(self, _lr):
        if isinstance(_lr, LR):
            self.lr = _lr
        else:
            raise TypeError("Please initiliztion this module with an instance of LRBench.lr.LR.")
    
    def plot(self, num_epoch = 10, title="Learning Rate Schedule",
             xlabel="#Epochs", ylabel="Learning Rate Values"):
        epochs = np.arange(num_epoch)
        lr_values = [self(i) for i in epochs]
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(epochs, lr_values)
        plt.title(title)
        plt.xlable(xlabel)
        plt.ylabel(ylabel)
    
    def __call__(self, epoch):
        return self.lr.getLR(epoch)