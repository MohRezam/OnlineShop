from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """
    Form for creating a new user account.

    This form allows administrators to create new user accounts. It includes fields
    for the user's email, phone number, first name, last name, image, and role. It also
    requires the user to input and confirm a password.

    Methods:
        clean_password2():
            Validates that the passwords entered in the password1 and password2 fields match.

        save(commit=True):
            Saves the user object with the hashed password.

        Returns:
            User: The newly created user object.
    """
    
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)
   
   
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'image' , 'role')
   
   
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd['password2']:
            raise ValidationError("passwords must match")
        return cd["password2"]
   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
   
class UserChangeForm(forms.ModelForm):
    """
    Form for changing user account details.

    This form allows administrators to change various details of a user account,
    including the email, phone number, first name, last name, image, password, and role.

    Attributes:
        password (ReadOnlyPasswordHashField): A read-only field for displaying the user's password
            hash and providing a link to change the password.

    Methods:
        save(commit=True):
            Saves the changes to the user account.

        Returns:
            User: The updated user object.
    """
    
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form.</a>")
   
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'image' , 'password' , 'role')