#method to perform grid search on a given model


from __future__ import print_function

from keras.layers import  Activation

import keras
# from keras.datasets import mnist
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

import numpy as np

# Added for LRBench
from keras.callbacks import LearningRateScheduler
# from LRBench.framework.keras.LearningRate import LearningRate
# from LRBench.lr.piecewiseLR import piecewiseLR

batch_size = 128
num_classes = 10
# epochs = int(epoch)

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print("connecting to Database")

# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

def get_model(learn_rate=0.01):
	model = Sequential()
	model.add(Conv2D(32, (3, 3), padding='same',
	                 input_shape=x_train.shape[1:]))
	model.add(Activation('relu'))
	model.add(Conv2D(32, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))

	model.add(Conv2D(64, (3, 3), padding='same'))
	model.add(Activation('relu'))
	model.add(Conv2D(64, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))

	model.add(Flatten())
	model.add(Dense(512))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(num_classes))
	model.add(Activation('softmax'))

	model.compile(loss=keras.losses.categorical_crossentropy,
	                  optimizer=keras.optimizers.Adadelta(lr=learn_rate),
	                  metrics=['accuracy','top_k_categorical_accuracy'])
	return model


x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
model_final = KerasClassifier(build_fn=get_model)
# define the grid search parameters


learn_rate = [0.5,0.75,1]
epochs = [30]


param_grid = dict(learn_rate=learn_rate, epochs=epochs)
grid = GridSearchCV(estimator=model_final, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(x_train, y_train)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))


#parameter grid - 
    