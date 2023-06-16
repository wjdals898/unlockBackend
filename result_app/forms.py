from django import forms
from .models import Prescription, Result
from django.forms import ModelForm

class PresForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ['result', 'content']

        labels = {
            'content':"처방전"
        }
        
        widgets = {
            'content':forms.Textarea(attrs={
                'rows':20,
                'cols':100,
                'placeholder':"처방전을 작성해주세요.",
            })
        }
        '''
        def __init__(self, user, *args, **kwargs):
            super(Result, self).__init__(*args, **kwargs)
            self.fields['result'].queryset = Result.objects.filter(id=user)
        '''
        