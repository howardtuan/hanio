from django import forms
from .models import member

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = member
        fields = ['MName', 'MPhone', 'MPW', 'MAccount', 'MEmail', 'MAddr', 'MVISA', 'MCK']