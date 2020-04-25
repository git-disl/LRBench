#This function is to give a rough outline of how to add 
#result to django sql db. We perform django.setup(), 
#then carry out the training as usual, and then 
# compute the metrics to be added to DB. Finally 
#the entry is added to the db

# Modified from the https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py by Yanzhao Wu

# from __future__ import print_function

import keras
# from keras.datasets import mnist
from keras.datasets import cifar10

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.layers import Dense, Dropout, Activation, Flatten

#needed to add to database
import django
django.setup()

# Added for LRBench
from keras.callbacks import LearningRateScheduler
from LRBench.framework.keras.LearningRate import LearningRate
from LRBench.lr.piecewiseLR import piecewiseLR

lrbenchLR = piecewiseLR([10,], [{'lrPolicy': 'SIN', 'k0': 1.0, 'k1':6.0, 'l': 5},
                                  {'lrPolicy': 'FIX', 'k0': 0.0001}])

lrCallback = [LearningRateScheduler(LearningRate(lrbenchLR), verbose=1)]

batch_size = 128
num_classes = 10
epochs = 1

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')
print("connecting to Database")

# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

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

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(lr=lrbenchLR.getLR(0)),
              metrics=['accuracy','top_k_categorical_accuracy'])

model_fit=model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test), callbacks=lrCallback)
print(model_fit.history['loss'])
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
#also TOP 1 accuracy
print('Test accuracy:', score[1])

#adding to the database after a successful run:
try:

  from LRBench.framework.keras.compute_metrics import compute_mertics
  
  #adding model name, data set name, model parameters
  project_dict=compute_mertics().add_parameters('Keras','cifar10',lrbenchLR)

  #adding robustness = testing accuracy - training accuracy
  #model_fit : return of model.fit
  #score : return of model.evaluate
  project_dict=compute_mertics().add_robustness(project_dict,model_fit,score)

  #adding top1, top5 accuracy
  #score : return of model.evaluate
  project_dict=compute_mertics().add_accuracy(project_dict,score)  

  #adding confidences
  model_predict=model.predict(x_test)
  project_dict=compute_mertics().add_confidence(project_dict,y_test,model_predict)
  print("Computed all metrics : ")
  print(project_dict)

  #pass the dictionary of the computed values to be added to datatbase
  from LRBench.database.db_utility import db_class
  db_class().add_result(project_dict)
  print("Result added to database")
  
except:
  print("Error in adding entry to database")


