from django import forms
from django.forms import formset_factory
from LRBench.models import LRSchedule

class LRForm(forms.Form):
    '''
    Main Form fields. 
    All fields are required. Saved schedules are retrieved from DB.
    '''
    DEFAULT_SCHEDULE= "Not using schedule"
    FRAMEWORK = (
        ('keras','Keras'), 
        ('caffe','Caffe'), 
        ('pytorch','PyTorch'),
    )
    DATASET = (
        ('cifar10','Cifar10'), 
        ('mnist','MNIST'),
    )

    #getting saved schedules from DB
    lr_schedule_entries=LRSchedule.objects.all()
    lr_schedule_dropdown=[ (x.id, x.lr_schedule_name ) for x in lr_schedule_entries ]
    lr_schedule_dropdown.insert(0, (0,DEFAULT_SCHEDULE))
    SAVED_SCHEDULES=(lr_schedule_dropdown)
    
    framework=forms.ChoiceField(label='Frame Work',choices=FRAMEWORK)
    dataset=forms.ChoiceField(label='Data Set',choices=DATASET)
    batch_size=forms.IntegerField(label='Batch size', min_value=1)
    saved_lr_schedules=forms.ChoiceField(label="Load LR Schedule",choices=SAVED_SCHEDULES,
        widget=forms.Select(attrs={"onChange": 'fill_lr_schedule(this)'}))

class LRPolicy(forms.Form):
    '''
    LRPolicy object which can be replicated according to the schedule we want to create.
    LRPolicy, Number of Epochs and k0 are required parameters. 
    Other parameters' requirement handled in JS.
    '''
    LR_CHOICES = (
        ('FIX', 'Fix'),
        ('STEP', 'Step'),
        ('SIN', 'Sin'),
        ('NSTEP', 'Nstep'),
        ('INV', 'Inv'),
        ('TRIEXP', 'TriExp'),
        ('EXP', 'Exp'),
        ('TRI','Tri'),
    )

    lrPolicy=forms.ChoiceField(label='LR Choices',choices=LR_CHOICES,widget=forms.Select(attrs={
     "onChange": 'lr_policy_change(this)',"required":'true'}), )
    epochs=forms.IntegerField(label='Number of epochs', min_value=1, widget=forms.NumberInput(attrs={"required":'true'}))
    k0=forms.FloatField(label='k0', widget=forms.NumberInput(attrs={"required":'true'}))
    k1=forms.FloatField(label='k1',required=False)
    p=forms.FloatField(label='p',required=False)
    gamma=forms.FloatField(label='gamma',required=False)
    l=forms.FloatField(label='l',required=False)
    lrSchedulerName=forms.CharField(label="LR Schedule Name", required=False)
LRFormset = formset_factory(LRPolicy, extra=1)