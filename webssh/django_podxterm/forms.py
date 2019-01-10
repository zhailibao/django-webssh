from django import forms
from django.forms import ModelForm
from .models import Container
class ContainerForm(ModelForm):
    namespace = forms.CharField(max_length=100,required=True)
    podname = forms.CharField(max_length=100,required=True)
    containername = forms.CharField(max_length=100,required=False)
    class Meta:
        model = Container
        fields = ['id','namespace', 'podname','containername']
        help_texts = {
            'labels':'{"namespace": "default","podname": "podname"}'
        }