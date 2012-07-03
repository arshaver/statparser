from django import forms

class UploadFileForm(forms.Form):
    file  = forms.FileField(required=True, label="Select the statistics text file")