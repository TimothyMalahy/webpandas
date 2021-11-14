valid_extensions_list = ['.xlsx', '.xls', '.txt', '.json', '.csv',]

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() in valid_extensions_list:
        raise ValidationError('Unsupported file extension.')
    
def valid_extensions():
    return "Acceptable file formats: *"+", *".join(valid_extensions_list)