from django.shortcuts import render
from .forms import LRForm,LRFormset
from django.forms import formset_factory
from django.http import HttpResponse
import importlib
from django.conf import settings


#main mr form process function
def lr_form_process(request):
    #if GET or any other method or invalid form, create a blank form
    form = LRForm()
    formset = LRFormset(request.GET or None) 
    template_name='base.html'
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        filename=(settings.STATIC_ROOT)[0]+"\\results.txt"
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
            result_file.write("Form is valid\n")
            dataset=form.cleaned_data['dataset']
            framework=form.cleaned_data['framework']+"_django"
            batch=form.cleaned_data['batch_size']
            epochs_list,total_epochs,lr_policies=call_specific_model(form.cleaned_data, formset_data)

            result_file.write("Selected dataset: " +dataset+"\n")
            result_file.write("Selected framework: " +form.cleaned_data['framework']+"\n")
            result_file.write("Epoch distribution selected: "+ str(epochs_list)+"\n")
            result_file.write("LR Policy distribution : "+ str(lr_policies)+"\n\n\n")
            result_file.write("Calling main LR function\n")
            result_file.close() #needed to refelct the change
            my_module = importlib.import_module("examples.%s.%s.%s" %(dataset,framework,framework))
            my_module.lr_main(batch,epochs_list,total_epochs,lr_policies)
          
            result_file=open(filename, "a+")
            result_file.write("Done!")
            result_file.close()
            return render(request, 'results.html')
    return render(request, template_name, {'formset': formset, 'form' : form})


#parsing into the required form
def call_specific_model(cleaned_form, cleaned_form_set):
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

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def home(request):
	return render(request, 'base.html', {'title': 'Home'})

def results(request):
    return render(request, 'results.html', {'title': 'Results'})
