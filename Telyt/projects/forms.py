from django import forms
from .models import Projects, Files

#custom project and file upload forms

class ProjectCreateForm(forms.ModelForm):
    project_name = forms.CharField(label="Project Name", max_length=100,required=True)

    class Meta:
        model = Projects
        fields = [
            'project_name',
        ]

class FileUploadForm(forms.Form):
    files = forms.FileField(
        label='Upload File',
        help_text='max. 42 megabytes'
    )