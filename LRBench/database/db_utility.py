from LRBench.models import Project
from LRBench.models import LRSchedule

class db_class:
	'''
	Method to save each successful run to DB.
	Table name: LRBench_project
	DB fields:
		primary key: auto generated integer 
		Fields obtained from Project model
	'''
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
		project.epochs=project_dict['epochs']
		project.save()

	'''
	Method to store lr schedules to DB
	Table name: LRBench_lrschedule
	DB fields:
		primary key: auto generated integer
		Fields obtained from LRSchedule model
	returns message to be displayed to user, bool: if the object was created
	'''
	def add_lr_schedule(self,lr_schedule_name,lr_policies,epochs_list):
		try:
			lr_schedule = LRSchedule()
			lr_schedule.lr_schedule_name=lr_schedule_name
			lr_schedule.lr_policy=lr_policies
			lr_schedule.epochs_list=epochs_list
			lr_schedule.save()
			return 'Saved LR Schedule!',True 
		except Exception as ex:
			return str(type(ex).__name__)+"   "+ str(ex.args),False