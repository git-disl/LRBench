import json
import importlib
import ast
from django.shortcuts import render
from LRBench.forms import LRForm, LRFormset
from django.conf import settings
from django.http import JsonResponse
from collections import OrderedDict
from django.core import serializers
from LRBench.models import LRSchedule
from LRBench.database.db_utility import db_class
from django.db import connection
'''
Main Form Processing method.
Validates the submitted form, parses to required format and calls NN to be run.
'''
def lr_form_process(request):
    #if GET or any other method or invalid form, create a blank form
    form = LRForm()
    formset = LRFormset(request.GET or None) 
    template_name='base.html'
    lrSchedules=get_lr_schedules_from_db()
   
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        filename=(settings.STATIC_ROOT)[0]+"/results.txt"
        result_file=open(filename, "w+")
        result_file.write("In LR form processing.\n")
        # create a form instance and populate it with data from the request:
        form = LRForm(request.POST)
        formset = LRFormset(request.POST)

        #Unlikely the form will be invaid as we are not allowing for
        #the users to submit without correct fields
        if form.is_valid() and formset.is_valid():
            formset_data=[]
            for f in formset: 
                formset_data.append(f.cleaned_data)

            #needed to handle loaded lr policies request
            if( "epochs" not in formset_data[0]):
                formset_data=formset_data[1:]

            result_file.write("Form is valid\n")
            dataset=form.cleaned_data['dataset']
            framework=form.cleaned_data['framework']+"_django"
            batch=form.cleaned_data['batch_size']
            epochs_list,total_epochs,lr_policies=call_specific_model(formset_data)

            #save the schedule if that option is selected
            if ("save-submit" in request.POST):
                lr_schedule_name=request.POST['lrScheduleName'].strip()
                epoch_list_full=epochs_list
                epoch_list_full.append(total_epochs-sum(epochs_list))  
                msg,is_saved=db_class().add_lr_schedule(lr_schedule_name,lr_policies,epoch_list_full)
                epochs_list=epochs_list[:-1]
                if not is_saved:
                    if 'UNIQUE constraint failed' in msg:
                        return render(request, template_name, {'formError':"LR Schedule Name already present. Please use another name next time."})
                    else:
                        return render(request, template_name, {'formError':msg})


            result_file.write("Selected dataset: " +dataset+"\n")
            result_file.write("Selected framework: " +form.cleaned_data['framework']+"\n")
            result_file.write("Epoch distribution selected: "+ str(epochs_list)+"\n")
            result_file.write("LR Policy distribution : "+ str(lr_policies)+"\n\n\n")
            result_file.write("Calling main LR function\n")
            result_file.close() #needed to reflect the change

            #calling the main NN implementation
            my_module = importlib.import_module("examples.%s.%s.%s" %(dataset,framework,framework))
            my_module.lr_main(batch,epochs_list,total_epochs,lr_policies)
          
            result_file=open(filename, "a+")
            #this string is matched to stop the xml http request while displaying results/logs
            result_file.write("Done!") 
            result_file.close()
            return render(request, 'results.html')
        else:
            render(request, template_name, {"formError":'Form not submitted.Please submit a valid form again.'})
    return render(request, template_name, {'formset': formset, 'form' : form, 'lrSchedules':lrSchedules })

'''Obtaining list of epochs, lr_policies and total number of epochs'''
def call_specific_model(cleaned_form_set):
    epochs=[]
    lr_policies=[]
    for ele in cleaned_form_set:
        epochs.append(ele['epochs'])
        new_dict={k: v for k, v in ele.items() if v is not None}
        new_dict.pop('epochs', None)
        lr_policies.append(new_dict)
    total_epochs=sum(epochs)
    epochs=epochs[:-1]
    return epochs,total_epochs,lr_policies

'''Parsing data for the visualization table'''
def pivot_data(request):
    #obtains data from only_logs.txt file
    filename=(settings.STATIC_ROOT)[0]+"/only_logs.txt"
    content=[]
    with open(filename) as f:
        for line in f:
            json_acceptable_string = line.replace("'", "\"").rstrip('\n')
            content.append(json.loads(json_acceptable_string,object_pairs_hook=OrderedDict))
    return JsonResponse(content, safe=False)
    
'''
Method returns lr policies to be used, when lr_schedule from DB is selected from dropdown. 
'''
def apply_lr_schedule(request):
    selection = request.GET.get('id',None)
    entry=LRSchedule.objects.get(pk=selection)
    #converting a string list to list
    epochs_list=ast.literal_eval(entry.epochs_list)
    lr_schedule=ast.literal_eval(entry.lr_policy)
    new_formset=create_formset(epochs_list,lr_schedule)  
    return JsonResponse(json.dumps(new_formset), safe=False)

'''
Includes epochs in the lr_policy instead of separate list
:epochs_list Ex:[20]
:lr_Schedule Ex:[{'lrPolicy': 'FIX', 'k0': 0.2}]
returns list with epochs Ex:[{'lrPolicy': 'FIX', 'k0': 0.2, 'epochs': 20}]
'''
def create_formset(epochs_list,lr_schedule):
    for i in range(len(epochs_list)):
        lr_schedule[i]['epochs']=epochs_list[i]
    return lr_schedule

''' Load LR Schedules from DB '''
def get_lr_schedules_from_db():
    #getting saved schedules from DB
    if 'LRBench_lrschedule' in connection.introspection.table_names():
        lr_schedule_entries=LRSchedule.objects.all()
        return lr_schedule_entries
    return []

def about(request):
    return render(request, 'about.html')

def home(request):
    return render(request, 'base.html')

def results(request):
    return render(request, 'results.html', {'title': 'Results/logs'})

def visualize(request):
    return render(request, 'visualize.html')