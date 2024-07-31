from django import forms

from .models import Plant


class PlantTreeForm(forms.Form):
    tree = forms.ModelChoiceField(
        queryset=Plant.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a latitude'
        })
    )
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a longitude'
        })
    )

class PlantMoreTreeForm(forms.Form):
    trees = forms.ModelMultipleChoiceField(
        queryset=Plant.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Seeds"
    )

