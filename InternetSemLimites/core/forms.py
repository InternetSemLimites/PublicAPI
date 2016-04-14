from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from InternetSemLimites.core.models import Provider


class ProviderForm(ModelForm):

    class Meta:
        model = Provider
        fields = ['category', 'name', 'url', 'source', 'coverage', 'other']
        widgets = {'coverage': CheckboxSelectMultiple()}
