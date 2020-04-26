'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

# Modified from the https://github.com/keras-team/keras/blob/master/examples/mnist_cnn.py by Yanzhao Wu
####UNcomeeeenttt
# from __future__ import print_function

import keras

from tensorflow.keras.datasets import boston_housing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import LambdaCallback


import sys
sys.path.append("C:\\alex\\spring 2020\\Special Problem\\LRBench\\")

# # Added for LRBench

from LRBench.framework.keras.LearningRate import LearningRate
from LRBench.lr.piecewiseLR import piecewiseLR




import tensorflow as tf

from django.conf import settings




# def keras_main(batch_size,epoch,parameters):
def lr_main(batch_size,epochs_list,total_epochs,lrPolicy):
# def lr_main():	
	try:
		print("in main keras function")
		filename=(settings.STATIC_ROOT)[0]+"\\results.txt"
		only_logs=(settings.STATIC_ROOT)[0]+"\\only_logs.txt"
		only_logs_file=open(only_logs, "w+")
		# filename="test.txt"

		result_file=open(filename, "a+")
		result_file.write("Reached main LR function\n")
		result_file.write("Batch size: "+ str(batch_size)+"\n")
		result_file.write("Total num_of_epochs: "+ str(total_epochs)+"\n")
		result_file.write("Epoch distribution : "+ str(epochs_list)+"\n")
		result_file.write("LR Policy distribution: "+ str(lrPolicy)+"\n")


		# num_of_epochs=sum(epochs_list)
		# num_of_epochs=10
		# print("number of epochs:: ", num_of_epochs)
		batch_size=batch_size


		lrbenchLR = piecewiseLR(epochs_list, lrPolicy)

		lrCallback = LearningRateScheduler(LearningRate(lrbenchLR), verbose=1)
		# Regression Example With Boston Dataset: Baseline

		# load dataset
		result_file.write("Reading dataset\n")	
		
		from keras.datasets import boston_housing
		
		(x_train, y_train), (x_test, y_test) = boston_housing.load_data()
		result_file.write("Reading dataset completed\n")

		result_file.write("Starting training model\n\n")		
		result_file.flush()
		model=wider_model(x_train,lrbenchLR)


		lcb = LambdaCallback(on_epoch_end= lambda epoch,logs:write_to_txt_file(epoch,logs,lrbenchLR,total_epochs,result_file,only_logs_file))

		history=model.fit(x_train,y_train,validation_split=0.2,epochs=total_epochs,callbacks=[lcb,lrCallback])

		output=model.evaluate(x_test,y_test)

		compute_results(history, output, result_file, x_test,y_test, model, lrbenchLR)

		result_file.write("Completed training model\n")
		result_file.write("Results mean::"+ str(output)+"\n")
		result_file.close()
		only_logs_file.close()
	except Exception as ex:
		filename=(settings.STATIC_ROOT)[0]+"\\results.txt"
		result_file=open(filename, "a+")
		result_file.write("Sorry! Run failed. Please try again\n")
		result_file.write(str(type(ex).__name__)+"      "+ str(ex.args)+"\n\n")
		result_file.close()

	
# define wider model
def wider_model(x_train,lrbenchLR):
	# create model
	model = Sequential()
	model.add(Dense(8,input_shape=[x_train.shape[1]],activation='relu'))
	model.add(Dense(16,activation='relu'))
	model.add(Dense(1))
	# Compile model

	model.compile(loss='mse', optimizer=tf.keras.optimizers.Adadelta(lr=lrbenchLR.getLR(0)),
	metrics=['accuracy','top_k_categorical_accuracy'])
	return model

def compute_results(model_fit,score, result_file, x_test, y_test,model, lrbenchLR):
	result_file.write("Computing the metrics : \n")
	from LRBench.framework.keras.compute_metrics import compute_mertics
	project_dict=compute_mertics().add_parameters('Keras','cifar10',lrbenchLR)
	project_dict=compute_mertics().add_robustness(project_dict,model_fit,score)
	project_dict=compute_mertics().add_accuracy(project_dict,score)  
	model_predict=model.predict(x_test)
	project_dict['average_confidence']=0
	project_dict['confidence_standard_deviation']=0
	project_dict['cdac']=0
	# project_dict=compute_mertics().add_confidence(project_dict,y_test,model_predict)
	result_file.write("Metrics are : "+str(project_dict)+"\n\n")
	from LRBench.database.db_utility import db_class
	db_class().add_result(project_dict)

	result_file.write("Result added to database\n\n")
	result_file.flush()

def write_to_txt_file(epochs,logs,lrbenchLR,total_epochs,result_file,only_logs_file):
	result_file.write("Epoch : " +str(epochs+1)+"/"+str(total_epochs)+"\n")
	result_file.write("Learning rate for epoch: "+str(epochs+1)+ " is "+ str(lrbenchLR.getLR(epochs))+"\n")
	result_file.write(str(logs)+"\n\n")
	result_file.flush()
	logs['epoch']=epochs+1
	logs['learning_rate']=lrbenchLR.getLR(epochs)
	only_logs_file.write(str(logs)+"\n")
	
	
	
	
	





# lr=[{'lrPolicy': 'FIX', 'k0': 1.1}, {'lrPolicy': 'FIX', 'k0': 0.0001}]
lr=[{'lrPolicy': 'SIN', 'k0': 1.0, 'k1':6.0, 'l': 5},
	                                  {'lrPolicy': 'FIX', 'k0': 0.0001}]
epochs=[10]
# lr_main(12,epochs,15,lr)
