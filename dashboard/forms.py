from django import forms
from .models import Expense
from bookings.models import Tour, Booking

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date_incurred']
        widgets = {'date_incurred': forms.DateInput(attrs={'type': 'date'})}

class SaleForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour', 'customer_name', 'customer_email', 'customer_phone', 'number_of_people', 'visitor_type', 'referral_code', 'total_price', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'visitor_type': forms.Select(choices=Booking.VISITOR_TYPE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.status = 'C' # Default to confirmed
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
        
        if 'visitor_type' in self.fields:
            self.fields['visitor_type'].widget.attrs['class'] = 'select w-full'
        if 'referral_code' in self.fields:
            self.fields['referral_code'].widget.attrs['placeholder'] = "e.g. CREW123"
        
        self.fields['total_price'].required = False
        self.fields['total_price'].help_text = "Leave blank for automatic calculation."