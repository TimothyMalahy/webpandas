from django.contrib import admin
from core.models import *

# Register your models here.


class DataFrameAdmin(admin.ModelAdmin):
    list_display = ('creator','name','dataframe')

admin.site.register(DataFrame, DataFrameAdmin)