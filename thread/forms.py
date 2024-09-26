"""
Thread form
"""

# Standard library imports.

# Related third party imports.
from django import forms

# Local application/library specific imports.
from .models import Thread


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['participants']

    def clean_participants(self):
        participants = self.cleaned_data.get('participants')
        if len(participants) > 2:
            raise forms.ValidationError("A thread can have a maximum of 2 participants.")
        return participants
