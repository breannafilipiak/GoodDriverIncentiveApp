from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import AllUsers, Driver, Sponsor, SponsorOrg


class Create_Account_Form(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=50, label=('First Name'), widget=forms.TextInput(attrs={'size': '75', 'placeholder':'John',}))
    last_name = forms.CharField(required=True, max_length=50,  label=('Last Name'), widget=forms.TextInput(attrs={'size': '75', 'placeholder':'Doe',}))
    email = forms.EmailField(required = True, label=("Email"), widget=forms.EmailInput(attrs={'size': '75', 'placeholder':'johndoe@gmail.com',}))
    
    class Meta:
        model = AllUsers
        fields = ('first_name', 'last_name', 'email')
     
    
class User_Login_Form(AuthenticationForm):
    username = forms.EmailField(label=("Email"), widget=forms.EmailInput(attrs={'size': '35', 'placeholder':'Email',})) 
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'size': '35', 'placeholder':'Password',}))

    def clean_email(self):
        email = self.cleaned_data['username']
        if AllUsers.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError(
                'Email does not exist')
        return email

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = AllUsers.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

class Edit_User_Info_Form(forms.ModelForm):

   first_name = forms.CharField(max_length=50, label=('First Name'), widget=forms.TextInput(attrs={'size': '75'}))
   last_name = forms.CharField(max_length=50,  label=('Last Name'), widget=forms.TextInput(attrs={'size': '75'}))
   email = forms.EmailField(label=("Email"), widget=forms.EmailInput(attrs={'size': '75'}))
   
   class Meta:
        model = AllUsers
        fields = ('first_name', 'last_name', 'email')

class Address_Form(forms.ModelForm):
    street_address = forms.CharField(max_length=150, label=('Street'), widget=forms.TextInput(attrs={'size': '75', 'placeholder': '123 Driver Lane',}),required=False)
    address_line = forms.CharField(max_length=150, label=('Address Line 2'), widget=forms.TextInput(attrs={'size': '75','placeholder': 'Apt A',}), required=False)
    city = forms.CharField(max_length=50, label=('City'), widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'Clemson',}),required=False)
    state = forms.CharField(max_length=2, label=('State'), widget=forms.TextInput(attrs={'size': '75', 'placeholder': 'SC',}),required=False)
    zip_code = forms.CharField(max_length=5, label=('Street'), widget=forms.TextInput(attrs={'size': '75', 'placeholder': '29630',}),required=False)

    class Meta:
        model = Driver
        fields = ('street_address', 'address_line', 'city', 'state', 'zip_code')

