from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Review, Hotel, Room

# -------------------------------
# User Registration Form
# -------------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# -------------------------------
# Booking Form
# -------------------------------
from django import forms
from .models import Booking

 

# main_app/forms.py
from django import forms
from .models import Booking

from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'total_price']
        widgets = {
            'check_in_date': forms.DateInput(attrs={
                'type': 'date',
                'id': 'check_in_date'
            }),
            'check_out_date': forms.DateInput(attrs={
                'type': 'date',
                'id': 'check_out_date'
            }),
            'total_price': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'placeholder': 'Total Price',
                'id': 'total_price'
            }),
        }

# -------------------------------
# Review Form
# -------------------------------
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select())
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Review
        fields = ["rating", "comment"]


# -------------------------------
# Hotel Form (Admin)
# -------------------------------
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "city", "description", "address", "rating", "image", "email", "password"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Hotel Name"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
        }
# -------------------------------
# Room Form (Admin)
# -------------------------------
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_number", "room_type", "price_per_night", "is_available", "image"]

