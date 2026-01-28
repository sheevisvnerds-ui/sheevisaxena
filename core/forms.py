from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PickupRequest, User

class PickupRequestForm(forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ['scrap_category', 'address', 'estimated_weight', 'scheduled_date']
        widgets = {
            'scrap_category': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter full address including landmark'}),
            'estimated_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Approx weight in Kg'}),
        }

class CustomerSignupForm(UserCreationForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        if commit:
            user.save()
        return user

class AgentSignupForm(UserCreationForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service Area / Base Address'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name', 'phone', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.AGENT
        if commit:
            user.save()
        return user
