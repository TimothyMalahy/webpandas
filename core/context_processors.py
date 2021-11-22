from core.models import *


# This is to provide context data on all pages

def dataframes_processor(request):
    return {
        'dataframes': DataFrame.objects.filter(creator=request.user.id)
    }