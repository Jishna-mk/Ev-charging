from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User


class UserAddForm(UserCreationForm):
    class Meta:
        model =User
        fields=["username","email","password1","password2"]

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)        

from django import forms
from .models import Booking
from django.forms import ValidationError



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time', 'phone_number', 'slot_number']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        available_slots = kwargs.pop('available_slots', None)
        booked_slots = kwargs.pop('booked_slots', None)
        super().__init__(*args, **kwargs)
        if available_slots is not None:
            choices = [(slot, slot) for slot in available_slots if slot not in booked_slots]
            self.fields['slot_number'] = forms.ChoiceField(choices=choices)