from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PickupRequest, User, PickupStatusUpdate

class PickupRequestForm(forms.ModelForm):
    pincode = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Pincode'}))
    
    class Meta:
        model = PickupRequest
        fields = ['scrap_category', 'address', 'pincode', 'estimated_weight', 'scheduled_date', 'latitude', 'longitude']
        widgets = {
            'scrap_category': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter full address including landmark'}),
            'estimated_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Approx weight in Kg'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
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

class ReschedulePickupForm(forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ['scheduled_date']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    
    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data['scheduled_date']
        # Add basic validation if needed, e.g. not in past
        return scheduled_date

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
        ('CUSTOMER', 'Customer'),
        ('AGENT', 'Pickup Agent'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), initial='CUSTOMER')
    
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service Area (Agents Only)'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('name', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
