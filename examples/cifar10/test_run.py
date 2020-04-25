#method to plot the outputs

from visualizer.plotLRAcc import plotLRAcc
from django_k import keras_cifar10
import numpy as np

# x_lr=np.array([10,20,30])
# y_acc=np.array([[60,70,80], [80,85,90]])
# colors=('g', 'b')
# y_acc_labels = [2.0, 20]

# plotLRAcc(x_lr, y_acc, colors, y_acc_labels, lr_str='(FIX, k)', fig_name='fig-lr.png')

#definning learning rate as :
x_lr=np.linspace(0.00001, 0.1, num=5)

#no of epochs
y_acc_labels = [1]

colors=('r')

# Getting y_acc
y_acc=keras_cifar10().cnn_model(x_lr,y_acc_labels)

plotLRAcc(x_lr, y_acc, colors, y_acc_labels, lr_str='(FIX, k)', fig_name='fig-lr.png')
