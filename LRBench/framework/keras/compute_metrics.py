
class compute_mertics:
	def p(self):
		print("in compte metrics class")

	def add_parameters(self,model_framework,dataset_name,model_params,epochs):
		project_dict={}
		project_dict['model_framework']=model_framework
		project_dict['dataset_name']=dataset_name
		project_dict['model_params']=model_params.toString()
		lr_functions=[]
		#extracting the models:
		for ele in model_params.LRparams:
			lr_functions.append(ele['lrPolicy'])
		project_dict['lr_policy']=str(lr_functions)	
		project_dict['epochs']=str(epochs)
		return project_dict

	def add_robustness(self,project_dict,model_fit,score):
		train_loss=score[0]
		test_loss = model_fit.history['loss'][-1]
		robustness= test_loss-train_loss
		project_dict['robustness']=robustness
		return project_dict

	def add_accuracy(self,project_dict,score):
  		project_dict['top_1_accuracy']=float(score[1])
  		project_dict['top_5_accuracy']=float(score[2])
  		return project_dict


	def add_confidence(self,project_dict,y_test,model_predict):
		import numpy as np
		prediction_labels=np.argmax(model_predict,axis=1)

		#getting the y labels into array 
		y_test_array=np.array(y_test)
		truth_labels=np.argmax(y_test_array,axis=1)

		#getting the maximum confidences for each entry
		max_confidences=np.amax(model_predict, axis=1)

		#getting the confidences for the matched labels
		matching_confidences=np.where(truth_labels==prediction_labels,max_confidences,0)
		#removing the 0s from the array to get only the matched values
		matching_confidences=matching_confidences[matching_confidences != 0]

		#find the average of the matched confidences
		average_confidence=np.mean(matching_confidences)
		print("Average Confidence: ", average_confidence)

		#find the standard deviation of the matched confidences
		confidence_standard_deviation=np.std(matching_confidences)
		print("Standard Deviation of confidences: ", confidence_standard_deviation)

		#getting only the indexes of the matchd labels
		matched_labels=np.where(truth_labels==prediction_labels,truth_labels,-1)
		matched_labels=matched_labels[matched_labels != -1]

		#create a dictionary where label is key, and put all the matching
		#confidences as a list for each key. 
		labels_confidences = dict()
		i=0
		for ele in matched_labels:
		    if ele in labels_confidences.keys():
		        labels_confidences[ele].append(matching_confidences[i])
		    else:
		        labels_confidences[ele]=[matching_confidences[i]]
		    i=i+1

		#store the average value of confidences class wise
		label_confidence_average=[]
		for i in range(len(labels_confidences)):
			# if the class was ever predicted
			if i in labels_confidences.keys():
				label_confidence_average.append(np.mean(np.array(labels_confidences[i])))
			else:
				label_confidence_average.append(0)


		cdac=np.std(np.array(label_confidence_average))
		print("CDAC", cdac)

		project_dict['average_confidence']=average_confidence
		project_dict['confidence_standard_deviation']=confidence_standard_deviation
		project_dict['cdac']=cdac

		return project_dict