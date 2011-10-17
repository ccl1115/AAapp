from django import forms
from AA.models import Expense

class NewExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ('host', 'pub_datetime')

class NewAccountForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(required=True, max_length=100)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)

