from django import forms
from .models import Booking, BookingLead
from tours.models import Tour


class BookingLeadForm(forms.ModelForm):
    TIME_SLOT_CHOICES = [
        ('Early Morning (06:30 - 08:30)', 'Early Morning (06:30 - 08:30) — Best for calm water & raptors'),
        ('Mid-Morning (08:30 - 11:30)', 'Mid-Morning (08:30 - 11:30) — Great for families & Crescent Island'),
        ('Afternoon (13:00 - 16:00)', 'Afternoon (13:00 - 16:00) — Scenic cruising'),
        ('Sunset Golden Hour (16:30 - 18:30)', 'Sunset Golden Hour (16:30 - 18:30) — Best for sunset & hippos'),
    ]

    preferred_time = forms.ChoiceField(choices=TIME_SLOT_CHOICES, required=True)
    adults = forms.IntegerField(min_value=1, initial=2, required=True)
    children = forms.IntegerField(min_value=0, initial=0, required=False)

    class Meta:
        model = BookingLead
        fields = [
            'name', 'phone', 'email', 'tour', 'trip_date',
            'preferred_time', 'adults', 'children', 'booking_type', 'notes'
        ]
        widgets = {
            'trip_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Special requests, photography focus, or arrival queries...'}),
        }

    def clean_children(self):
        return self.cleaned_data.get('children') or 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tour'].queryset = Tour.objects.filter(is_active=True).order_by('sort_order')
        self.fields['tour'].empty_label = "Select a Lake Naivasha Experience"
        
        # Style all form fields consistently
        for name, field in self.fields.items():
            classes = "form-input"
            if isinstance(field.widget, forms.Select):
                classes = "form-select"
            elif isinstance(field.widget, forms.Textarea):
                classes = "form-textarea"
            field.widget.attrs.update({'class': classes})


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'number_of_people', 'visitor_type', 'currency', 'referral_code', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
