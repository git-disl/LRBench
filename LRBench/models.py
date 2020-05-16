from django.db import models
from django.utils import timezone

class Project(models.Model):
  '''
  Model of Project entity to be stored in DB after successful run.
  Project features:
    model_fracmework: a string, Ex Keras.
    dataset_name: a string, Ex Cifar-10
    lr_policy: a string list, Ex '[SIN,FIX]'
    model_params: a string of parameters corresponding to the lr_policy
            Ex: [{'lrPolicy': 'SIN', 'k0': 1.0, 'k1':6.0, 'l': 5},{'lrPolicy': 'FIX', 'k0': 0.0001}]
    the rest are metrics computed according to paper  
  '''  
  model_framework=models.CharField(max_length=1000)
  model_params=models.TextField(max_length=1000)
  epochs=models.TextField()
  lr_policy=models.CharField(max_length=100)
  dataset_name=models.CharField(max_length=1000)
  testing_accuracy=models.FloatField(default=0)
  top_5_accuracy=models.FloatField(default=0)
  average_confidence=models.FloatField(default=0)
  std_dev_confidence=models.FloatField(default=0)
  cdac=models.FloatField(default=0)
  robustness=models.FloatField(default=0)
  date_finished = models.DateTimeField(default=timezone.now)

class LRSchedule(models.Model):
  '''
  Model of LRSchedule.
  lr_policy:a string of parameters corresponding to the lr_policy
          Ex: [{'lrPolicy': 'SIN', 'k0': 1.0, 'k1':6.0, 'l': 5},{'lrPolicy': 'FIX', 'k0': 0.0001}]
  epochs_list:a string corresponding to number of epochs for each policy
          Ex:[10,20]
  '''
  lr_schedule_name=models.CharField(max_length=1000, unique=True)
  lr_policy=models.TextField()
  epochs_list=models.TextField()
  date_added = models.DateTimeField(default=timezone.now)