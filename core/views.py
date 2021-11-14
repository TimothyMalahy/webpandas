from django.http.response import HttpResponse, Http404
from django.utils import datastructures
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.shortcuts import render
from core.models import *
from core.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import pandas as pd
from re import findall
from bs4 import BeautifulSoup as Soup

# Create your views here.

def Home(request):
    html = "<html><body>test</body></html>"
    return HttpResponse(html, status=200)


class SubmitDataframe(CreateView):
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
    dataframes = DataFrame.objects.filter(creator=request.user.id)
    context = {
        'dataframes':dataframes
    }
    return render(request, 'core/viewdatas.html', context) 


def Manipulate(request, id):
    obj = DataFrame.objects.filter(pk=id).first()
    df_web = obj.dataframe
    df = pd.read_csv(df_web)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # output = df.to_html(index=None)


    output = clean_df(df)

    context = {
        'output':output,
    }
    return render(request, 'core/output.html', context)


def Ajax_FindAndReplace(request, id, column):
    obj = DataFrame.objects.filter(pk=id).first()
    df_web = obj.dataframe
    


# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404



def clean_df(df):
    # print(df)
    html = df.to_html(index=True)
    columns = len(df.columns)+1
    html = re.sub('border="1" ',"",html)
    html = re.sub('class="dataframe"', 'class="dataframe table table-bordered"', html)
    #thead
    # TODO find the nth occurence of the header to give the columns index
    # TODO find a way to enter a new row in the Thead area to put the buttons above the columns names
    html = re.sub('<tr style="text-align: right;">','<tr>', html)
    html = re.sub('<th>',
    '''<th scope="col">
            <button type="button" class="btn btn-primary findandreplace">
                <a>find and replace</a>
            </button>
            <button type="button" class="btn btn-danger">
                <i class="material-icons">delete</i>
            </button>
    ''',html, columns)

    return html

