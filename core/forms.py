from django import forms

from .models import QuoteRequest


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            "name", "company", "phone", "email", "service",
            "origin", "destination", "cargo_type", "weight",
            "movement_date", "release_time", "closing_time", "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "company": forms.TextInput(attrs={"placeholder": "Company (optional)"}),
            "phone": forms.TextInput(attrs={"placeholder": "+254 7XX XXX XXX"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com"}),
            "origin": forms.TextInput(attrs={"placeholder": "e.g. CFS, Mombasa"}),
            "destination": forms.TextInput(attrs={"placeholder": "e.g. Industrial Area, Nairobi"}),
            "cargo_type": forms.TextInput(attrs={"placeholder": "e.g. palletised building materials"}),
            "weight": forms.TextInput(attrs={"placeholder": "e.g. 12 tonnes"}),
            "movement_date": forms.DateInput(attrs={"type": "date"}),
            "release_time": forms.TextInput(attrs={"placeholder": "If awaiting release"}),
            "closing_time": forms.TextInput(attrs={"placeholder": "e.g. store closes 4 pm"}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Receiving contact, access restrictions, anything else"}),
        }
