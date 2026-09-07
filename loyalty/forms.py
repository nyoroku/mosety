from django import forms
from .models import LoyaltyMember

class LoyaltySignupForm(forms.ModelForm):
    class Meta:
        model = LoyaltyMember
        fields = ['customer_name', 'email']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-6 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-ocean/20 focus:border-ocean outline-none transition-all placeholder:text-slate-400 font-medium',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-6 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-2 focus:ring-ocean/20 focus:border-ocean outline-none transition-all placeholder:text-slate-400 font-medium',
                'placeholder': 'Email Address'
            }),
        }
