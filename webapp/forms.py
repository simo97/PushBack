from django.forms import ModelForm, HiddenInput
from core.models import Application


class CreateApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = ['name', 'description', 'account', ]
        widgets = {
            'account': HiddenInput()
        }
