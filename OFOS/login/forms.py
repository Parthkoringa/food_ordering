from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomeUser

class Registration(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ["username","email","contact","usertype","address","password1","password2"]
        
    # class Loginform(forms.Form):
    #     username = forms.CharField()
    #     password = forms.CharField(widget=forms.PasswordInput)
        
    def save(self, commit=True):
        user = super(Registration, self).save(commit=False)
        user.usertype = self.cleaned_data['usertype']
        user.email = self.cleaned_data['email']
        user.contact = self.cleaned_data['contact']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user