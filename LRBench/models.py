from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from django.urls import reverse
import os

class Project(models.Model):

  
  model_framework=models.CharField(max_length=1000)
  model_params=models.TextField(max_length=1000)
  lr_policy=models.CharField(max_length=100)
  dataset_name=models.CharField(max_length=1000)
  testing_accuracy=models.FloatField(default=0)
  top_5_accuracy=models.FloatField(default=0)
  average_confidence=models.FloatField(default=0)
  std_dev_confidence=models.FloatField(default=0)
  cdac=models.FloatField(default=0)
  robustness=models.FloatField(default=0)
  date_finished = models.DateTimeField(default=timezone.now)

   
  def __str__(self):
    return self.title
  def extension(self):
	  name, extension = os.path.splitext(self.file.name)
	  return extension

  def get_absolute_url(self):
	  return reverse('post-detail', kwargs={'pk': self.pk})


