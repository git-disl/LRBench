#Simple cnn model for cifar 10 dataset
import keras
import tensorflow as tf
from keras.datasets import cifar10
from tensorflow.keras.datasets import boston_housing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import LambdaCallback
# # Added for LRBench
from LRBench.framework.keras.LearningRate import LearningRate
from LRBench.lr.piecewiseLR import piecewiseLR
from django.conf import settings
from LRBench.framework.keras.compute_metrics import compute_mertics
from LRBench.database.db_utility import db_class

def lr_main(batch_size,epochs_list,total_epochs,lrPolicy):	
	try:
		num_classes = 10
		filename=(settings.STATIC_ROOT)[0]+"/results.txt"
		only_logs=(settings.STATIC_ROOT)[0]+"/only_logs.txt"
		only_logs_file=open(only_logs, "w+")
		result_file=open(filename, "a+")
		result_file.write("Reached main LR function\n")
		result_file.write("Batch size: "+ str(batch_size)+"\n")
		result_file.write("Total num_of_epochs: "+ str(total_epochs)+"\n")
		result_file.write("Epoch distribution : "+ str(epochs_list)+"\n")
		result_file.write("LR Policy distribution: "+ str(lrPolicy)+"\n")

		batch_size=batch_size
		lrbenchLR = piecewiseLR(epochs_list, lrPolicy)
		lrCallback = LearningRateScheduler(LearningRate(lrbenchLR), verbose=1)

		# load dataset
		result_file.write("Reading dataset\n")			
		(x_train, y_train), (x_test, y_test) = cifar10.load_data()
		y_train = keras.utils.to_categorical(y_train, num_classes)
		y_test = keras.utils.to_categorical(y_test, num_classes)
		x_train = x_train.astype('float32')
		x_test = x_test.astype('float32')
		x_train /= 255
		x_test /= 255
		result_file.write("Reading dataset completed\n")

		result_file.write("Starting training model\n\n")		
		result_file.flush()
		model=wider_model(x_train,lrbenchLR)
		lcb = LambdaCallback(on_epoch_end= lambda epoch,logs:write_to_txt_file(epoch,logs,lrbenchLR,total_epochs,result_file,only_logs_file))
		history=model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=total_epochs,
          verbose=1,
          validation_data=(x_test, y_test), callbacks=[lcb,lrCallback])
		output=model.evaluate(x_test,y_test)
		epochs_complete_list=epochs_list
		epochs_complete_list.append(total_epochs-sum(epochs_list))
		compute_results(history, output, result_file, x_test,y_test, model, lrbenchLR,epochs_complete_list)
		result_file.write("Completed training model\n")
		result_file.write("Results mean::"+ str(output)+"\n")
		result_file.close()
		only_logs_file.close()
	except Exception as ex:
		filename=(settings.STATIC_ROOT)[0]+"/results.txt"
		result_file=open(filename, "a+")
		result_file.write("Sorry! Run failed. Please try again\n")
		result_file.write(str(type(ex).__name__)+"      "+ str(ex.args)+"\n\n")
		result_file.close()

	
# define wider model
def wider_model(x_train,lrbenchLR):
	num_classes=10
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


	# Compile model
	model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=tf.keras.optimizers.Adadelta(lr=lrbenchLR.getLR(0)),
              metrics=['accuracy','top_k_categorical_accuracy'])
	return model

def compute_results(model_fit,score, result_file, x_test, y_test,model, lrbenchLR,epochs):
	result_file.write("Computing the metrics : \n")
	project_dict=compute_mertics().add_parameters('Keras','cifar10',lrbenchLR,epochs)
	project_dict=compute_mertics().add_robustness(project_dict,model_fit,score)
	project_dict=compute_mertics().add_accuracy(project_dict,score)  
	model_predict=model.predict(x_test)
	project_dict=compute_mertics().add_confidence(project_dict,y_test,model_predict)
	result_file.write("Metrics are : "+str(project_dict)+"\n\n")
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
	temp=dict(sorted(logs.items()))
	only_logs_file.write(str(temp)+"\n")