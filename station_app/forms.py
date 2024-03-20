from django.forms import ModelForm
from django.forms import TextInput,Textarea,NumberInput,DateInput
from .models import StationProfile


class StationProfileForm(ModelForm):
    class Meta:
        model = StationProfile
        fields = ["Address","Phone_Number","Profile_Image"]

        widgets = {
            'Phone_Number': TextInput(attrs={"class":"form-control","placeholder":"Enter Phone number"}),
           
            'Address': Textarea(attrs={"class":"form-control","placeholder":"Enter  Address"}),
           
        }


from django import forms
from .models import Station

class StationForm(forms.ModelForm):
    class Meta:
        model = Station  
        fields = '__all__'
