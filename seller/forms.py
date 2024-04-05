from .models import Pin, SellerInfo
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class SellerRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	username = forms.CharField(label=("Mobile Number/Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	shop = forms.CharField(label=("Shop Name"),widget=forms.TextInput(attrs={}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'shop']

class SellerAddressForm(forms.ModelForm):
	shop_Address = forms.CharField(widget=forms.TextInput(attrs={}))
	shop_Name = forms.CharField(widget=forms.TextInput(attrs={}))
	locality = forms.CharField(required =True)
	city = forms.CharField(required =True)
	alternate_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	landmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landmark(optional)'}), required = False)
	class Meta:
		model = SellerInfo
		fields = [
			'mobile',
			'shop_Name',
			'alternate_mobile',
			'shop_Address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]

class UpdateSellerDetailForm(forms.ModelForm):
	class Meta:
		model = SellerInfo
		fields = [
			'photo',
			'mobile',
			'seller_Name',
			'alternate_mobile',
			'seller_Address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]

class UpdateSellerAccountDetailForm(forms.ModelForm):
	class Meta:
		model = SellerInfo
		fields = [
			'account_Holder_Name',
			'account_Number',
			'ifsc_Code',
			]