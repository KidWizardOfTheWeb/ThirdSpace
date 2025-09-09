from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget
from .models import User, NotificationSettings, UserPageData

from django.contrib.auth.forms import UserCreationForm

# from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, required=True,
                               widget=forms.TextInput(attrs={'placeholder' : 'Username'
                                                             }))
    password = forms.CharField(max_length=50, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

    class Meta:
        model = User
        fields = ["username", "password"]

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=32, required=True,
                               widget=forms.TextInput(attrs={'placeholder' : 'Username','class':'form-control'
                                                             }))
    first_name = forms.CharField(max_length=50, required=True,
                            widget=forms.TextInput(attrs={'placeholder' : 'First Name', 'class':'form-control'}))
    last_name = forms.CharField(max_length=50, required=True,
                            widget=forms.TextInput(attrs={'placeholder' : 'Last Name','class':'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder' : 'Email','class':'form-control'}))
    phone = PhoneNumberField(region="US", max_length=17,
                             widget = RegionalPhoneNumberWidget(attrs={'placeholder' : 'Phone Number',
                                                                       'type': 'tel','class':'form-control'}))
    password1 = forms.CharField(max_length=50, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder' : 'Password','class':'form-control'}))
    password2 = forms.CharField(max_length=50, required=True,
                                       widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm Password','class':'form-control'}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "password1", "password2"]

# class RegisterSponsorForm(UserCreationForm):
#     username = forms.CharField(max_length=32, required=True,
#                                widget=forms.TextInput(attrs={'placeholder' : 'Username','class':'form-control'
#                                                              }))
#     first_name = forms.CharField(max_length=50, required=True,
#                             widget=forms.TextInput(attrs={'placeholder' : 'First Name', 'class':'form-control'}))
#     last_name = forms.CharField(max_length=50, required=True,
#                             widget=forms.TextInput(attrs={'placeholder' : 'Last Name','class':'form-control'}))
#     job_title = forms.CharField(max_length=100,
#                             widget=forms.TextInput(attrs={'placeholder' : 'Job Title','class':'form-control'}))
#     email = forms.EmailField(required=True,
#                              widget=forms.TextInput(attrs={'placeholder' : 'Email','class':'form-control'}))
#     phone = PhoneNumberField(region="US", max_length=17,
#                              widget = RegionalPhoneNumberWidget(attrs={'placeholder' : 'Phone Number',
#                                                                        'type': 'tel','class':'form-control'}))
#     password1 = forms.CharField(max_length=50, required=True,
#                                widget=forms.PasswordInput(attrs={'placeholder' : 'Password','class':'form-control'}))
#     password2 = forms.CharField(max_length=50, required=True,
#                                        widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm Password','class':'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ["first_name", "last_name", "username", "email", "phone", "password1", "password2"]



class ResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder' : 'Enter email'}))

class PasswordConfirmationForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    email_code = forms.CharField(max_length=6, required=True, label='Confirmation code',
                                 widget=forms.TextInput(attrs={'placeholder' : 'Enter code sent to email'}))
    new_password = forms.CharField(label='New Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    def check_password(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('new_password')
        if new_password != confirm_password:
            # should be self.add_error("Passwords do not match.") no?
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(label='Current Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Enter current password'}))
    new_password = forms.CharField(label='New Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    def check_password(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('new_password')
        if new_password != confirm_password:
            # should be self.add_error("Passwords do not match.") no?
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class ConfirmationCodeForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    email_code = forms.CharField(max_length=6, required=True, label='Confirmation code',
                                 widget=forms.TextInput(attrs={'placeholder' : 'Enter code sent to email'}))

class EditProfileForm(forms.ModelForm): # forms.ModelForm to extend Model
    phone_number = PhoneNumberField(region="US", max_length=17,
                             widget = RegionalPhoneNumberWidget(attrs={'placeholder' : 'Phone Number',
                                                                       'type': 'tel',}))
    class Meta():
        model = User
        fields = ['picture', 'first_name', 'last_name', 'email', 'phone_number', 'bio']

# class EditSponsorForm(forms.ModelForm):
#     class Meta():
#         model = Sponsor
#         fields = ['logo', 'banner', 'bio', 'link']

# class EditAddressForm(forms.ModelForm): # forms.ModelForm to extend Model
#     class Meta():
#         model = Address
#         fields = ['type', 'name', 'address_1', 'address_2', 'city', 'state', 'country', 'zip_code']

class SettingsChangePasswordForm(forms.Form):
    current_password = forms.CharField(label="Current Password", widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}),
                                       required=True)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
                                       required=True)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
                                       required=True)

    def check_password(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('new_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ChangePointsForm(forms.Form):
    points = forms.IntegerField(label="Points to add/subtract, use a negative value to subtract points.")
    reason = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'name': 'body', 'rows': "5", 'cols': "20"}))

class SponsorSettingsForm(forms.ModelForm):
    point_rate = forms.FloatField(label="Point-to-Dollar Ratio", min_value=1,
                                  widget=forms.NumberInput(attrs={'step': 0.01}))

    # class Meta:
    #     model = Sponsor
    #     fields = ['banner', 'logo', 'company_email', 'link', 'point_rate', 'allow_negative_balance', 'bio'] #, 'suspend_points_until']

class DriverNotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = [
            'delivery_notification',
            'shipped_notification',
            'catalog_notification',
            'point_change_notification',
            'purchase_notification',
            'approvals_notification',
            'sponsor_notification',
            'rate_change_notification'
        ] # need to add more!

# class DriverTicketForm(forms.ModelForm):
#     sponsor = forms.ModelChoiceField(
#         queryset=Sponsor.objects.none(),
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-select'}),
#         label="Select Sponsor"
#     )
#
#     class Meta:
#         model = Tickets
#         fields = ['type', 'description', 'sponsor']
#         widgets = {
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'type': forms.Select(attrs={'class': 'form-select'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if user and hasattr(user, 'driver'):
#             self.fields['sponsor'].queryset = user.driver.sponsor.all()  # Filter sponsors
#         else:
#             self.fields['sponsor'].queryset = Sponsor.objects.none()
#
# class SponsorTicketForm(forms.ModelForm):
#
#     class Meta:
#         model = Tickets
#         fields = ['type', 'description']
#         widgets = {
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#             'type': forms.Select(attrs={'class': 'form-select'}),
#         }
#
#
# class TicketResponseForm(forms.ModelForm):
#     class Meta:
#         model = TicketResponse
#         fields = ['message']


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCEWidget(attrs={'cols': 80, 'rows':30,'class': 'form-control'}))
    class Meta:
        model = UserPageData
        fields = ['content']

class SearchEngineForm(forms.Form):
    # What the user enters into the search box
    # note: check if "required" is necessary (depends on final page design honestly)
    searchBoxQuery = forms.CharField(required=True,
                               widget=forms.SearchInput(attrs={'placeholder' : 'Find your ThirdSpace',
                                                               'autocomplete':'off',
                                                               'inputmode':'search'}), label='')