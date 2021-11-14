from django.urls import path
from core import views
from .views import *

app_name = "core" 

urlpatterns = [
    path('', Home, name='home'),
    path('submit/', views.SubmitDataframe.as_view(), name='submitdataframe'),
    path('view/', views.ViewDatas, name='listdatas'),
    path('manipulate/<id>/', views.Manipulate, name='manipulate'),
    path('ajax/findandreplace/id/', views.Ajax_FindAndReplace, name='findandreplace')
]