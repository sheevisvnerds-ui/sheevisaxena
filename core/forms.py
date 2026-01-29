from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PickupRequest, User, PickupStatusUpdate

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

class PickupStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = PickupStatusUpdate
        fields = ['status', 'location', 'description']
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., On the Way, Arrived'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional details...'}),
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

class UnifiedSignupForm(UserCreationForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    
    ROLE_CHOICES = [
        ('CUSTOMER', 'I want to Sell Scrap'),
        ('AGENT', 'I want to become a Pickup Partner'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'btn-check'}), initial='CUSTOMER')
    
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service Area (Agents Only)'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name', 'phone', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
