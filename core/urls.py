from django.urls import path
from core import views
from .views import *

app_name = "core" 

urlpatterns = [
    path('', views.Home, name='home'),
    path('submit/', views.SubmitDataframe.as_view(), name='submitdataframe'),
    path('view/', views.ViewDatas, name='viewdatas'),
    path('manipulate/<id>/', views.Manipulate, name='manipulate'),
    path('ajax/savedataframe', views.Ajax_SaveDataFrame, name='savedataframe')
]