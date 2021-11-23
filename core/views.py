from django.http.response import HttpResponse, Http404
from django.utils import datastructures
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.shortcuts import render
from core.models import *
from core.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
import os
import pandas as pd

# Create your views here.

def Home(request):
    '''
    This is the home page
    '''
    context = {
        '':'',
    }
    return render(request, 'core/home.html', context)


class SubmitDataframe(CreateView):
    '''
    Form for submitting dataframes
    '''
    model = DataFrame
    form_class = UploadDataFrame
    template_name = 'core/submitdataframe.html'


    def get_form_kwargs(self):
        kwargs = super(SubmitDataframe, self).get_form_kwargs()
        kwargs.update({'creator':self.request.user.id})
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('core:submitdataframe'))

    def form_valid(self, form):
        print(form)
        form = form.cleaned_data
        DataFrame.objects.create(creator=form['creator'], name=form['name'], dataframe=form['dataframe'])
        return HttpResponseRedirect(reverse('core:submitdataframe'))


def ViewDatas(request):
    '''
    This is to view all the dataframes owned by the user
    '''
    dataframes = DataFrame.objects.filter(creator=request.user.id).exclude(dataframe__exact='')
    baddataframes = len(DataFrame.objects.filter(creator=request.user.id).filter(dataframe__exact=''))
    
    context = {
        'dataframes':dataframes,
        'baddataframes':baddataframes
    }
    return render(request, 'core/viewdatas.html', context) 


def Manipulate(request, id):
    '''
    This is the editing page
    '''
    obj = DataFrame.objects.filter(pk=id).first()
    df_web = obj.dataframe
    df = pd.read_csv(df_web)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # output = df.to_html(index=None)


    output = clean_df(df)

    context = {
        'output':output,
    }
    return render(request, 'core/manipulate.html', context)



def Ajax_SaveDataFrame(request):
    '''
    Passes dataframe back to panda to save it
    '''
    
    
    path = 'media/core/temp/'+str(request.user.id)+'/outputs/'
    isExist = os.path.exists(path)

    if not isExist:
        os.makedirs(path)

    data = json.loads(request.GET['string'])
    df = pd.DataFrame.from_dict(data)
    df.columns = df.iloc[0]
    df = df[1:]
    df.to_csv(path+'output.csv')
    pathid = request.GET['pathname'].split('/')[-2]



    obj = DataFrame.objects.filter(pk=pathid).first()
    obj.dataframe = 'core/temp/'+str(request.user.id)+'/outputs/output.csv'
    obj.save()
    print(obj, obj.dataframe)
    
    
    return HttpResponse("Success!") # Sending an success response


def clean_df(df):
    '''
    Function to clean the dataframes submitting in SubmitDataFrame
    '''
    # print(df)
    html = df.to_html(index=True)
    columns = len(df.columns)+1
    html = re.sub('border="1" ',"",html)
    html = re.sub('class="dataframe"', 'class="dataframe table table-bordered"', html)
    html = re.sub('<tr style="text-align: right;">','<tr>', html)


    return html
