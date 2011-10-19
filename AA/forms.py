from django import forms
from django.contrib.auth.models import User
from AA.models import Expense

class NameModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()
        
class NewExpenseForm(forms.Form):
    money = forms.FloatField(required=True)
    title = forms.CharField(required=True, max_length=100)
    participants = NameModelMultipleChoiceField(required=True, queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple)

class NewAccountForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(required=True, max_length=100)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)

