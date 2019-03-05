from django import forms

from .models import ProfileUser

class RegisterUser(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = ProfileUser
		fields = ('name', 'username', 'password', 'email', 'mobile', 'is_vendor')