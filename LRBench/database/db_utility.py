'''
framework: a string. Example: keras
parameters: a list of dictionaries. Example : [{'lrPolicy': 'SIN', 'k0': 1.0, 'k1':6.0, 'l': 5},
			{'lrPolicy': 'FIX', 'k0': 0.0001}]
dataset: a string. Example:mnist

testing_accuracy: Float representing the testing accuracy

robustness:training accuracy-testing accuracy


'''
from LRBench.models import Project
class db_class:
	
	def add_result(self,project_dict):
		project = Project()
		project.model_framework = project_dict['model_framework']
		project.dataset_name=project_dict['dataset_name']
		project.lr_policy=project_dict['lr_policy']
		project.model_params = project_dict['model_params']
		project.testing_accuracy=project_dict['top_1_accuracy']
		project.top_5_accuracy=project_dict['top_5_accuracy']
		project.robustness=project_dict['robustness']
		project.average_confidence=project_dict['average_confidence']
		project.std_dev_confidence=project_dict['confidence_standard_deviation']
		project.cdac=project_dict['cdac']
		project.save()
