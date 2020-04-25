#Main forms file defining required fields.

from django import forms
from django.forms import formset_factory

class LRForm(forms.Form):

    LR_CHOICES = (
        ('FIX', 'Fix'),
        ('STEP', 'Step'),
        ('SIN', 'Sin'),
    )
    FRAMEWORK = (
        ('keras','Keras'), 
        ('caffe','Caffe'), 
        ('pytorch','PyTorch'),
    )
    DATASET = (
        ('cifar10','Cifar10'), 
        ('mnist','MNIST'),
    )
    framework=forms.ChoiceField(label='Frame Work',choices=FRAMEWORK)
    dataset=forms.ChoiceField(label='Data Set',choices=DATASET)
    batch_size=forms.IntegerField(label='Batch size', min_value=1)
    

class LRPolicy(forms.Form):
    LR_CHOICES = (
        ('FIX', 'Fix'),
        ('STEP', 'Step'),
        ('SIN', 'Sin'),
        ('NSTEP', 'Nstep'),
        ('INV', 'Inv'),
        ('TRIEXP', 'TriExp'),
        ('EXP', 'Exp'),
    )
    lrPolicy=forms.ChoiceField(label='LR Choices',choices=LR_CHOICES,widget=forms.Select(attrs={
     "onChange": 'lr_policy_change(this)',"required":'true'}), )
    epochs=forms.IntegerField(label='Number of epochs', min_value=1, widget=forms.NumberInput(attrs={"required":'true'}))
    k0=forms.FloatField(label='k0', widget=forms.NumberInput(attrs={"required":'true'}))
    k1=forms.FloatField(label='k1',widget=forms.NumberInput(attrs={"disabled":'true'}), required=False)
    p=forms.FloatField(label='p',widget=forms.NumberInput(attrs={"disabled":'true'}), required=False)
    gamma=forms.FloatField(label='gamma',widget=forms.NumberInput(attrs={"disabled":'true'}), required=False)
    l=forms.FloatField(label='l',widget=forms.NumberInput(attrs={"disabled":'true'}),  required=False)

LRFormset = formset_factory(LRPolicy, extra=1)
