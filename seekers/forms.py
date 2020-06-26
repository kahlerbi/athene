from django import forms

class EmailForm(forms.Form):
    email_content = forms.CharField(label='email_content', max_length=5000)