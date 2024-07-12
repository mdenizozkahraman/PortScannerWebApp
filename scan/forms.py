from django import forms

class InputForm(forms.Form):
    ip_address = forms.CharField(label='IP Address or Domain')
    ports = forms.CharField(label='Ports (optional)', required=False, help_text='(e.g., 80 443 21 or 80-90)')
