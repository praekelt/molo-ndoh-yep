# import re
from django import forms
# from PIL import Image
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from django.core.exceptions import ValidationError
import time


class RegistrationForm(forms.Form):

    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Username"),
        error_messages={'invalid': _("This value must contain only letters, \
         numbers and underscores.")})
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=dict(
                required=True,
                max_length=4,
                render_value=False,
                type='password')),
        label=_("PIN"))
    year = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'number'}),
        label=_("Year"))
    month = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'number'}),
        label=_("Month"))
    day = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'number'}),
        label=_("Day"))

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username']
                )
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("Username is already exists!"))

    def clean_password1(self):
        pin = self.cleaned_data['password1']
        length_of_pin = len(str(pin))
        if length_of_pin != 4:
            raise forms.ValidationError(u'Please enter 4 digit numnber')
        return pin

    def clean_year(self):
        year = self.cleaned_data['year']
        thisyear = time.localtime()[0]
        length_of_year = len(str(year))
        if year > thisyear or length_of_year != 4 or year < 1900:
            raise forms.ValidationError(u'Please enter a valid year')
        return year

    def clean_month(self):
        month = self.cleaned_data['month']
        length_of_month = len(str(month))
        if length_of_month > 2 or month == 0:
            raise forms.ValidationError(u'Please enter a valid month')
        return month

    def clean_day(self):
        day = self.cleaned_data['day']
        length_of_day = len(str(day))
        if length_of_day > 2 or day == 0:
            raise forms.ValidationError(u'Please enter a valid day')
        return day

    def clean(self):
        return self.cleaned_data


class EditProfileForm(RegistrationForm):
    alias = forms.CharField(
        label=_("Display Name"),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['year']
        del self.fields['month']
        del self.fields['day']
        del self.fields['username']
        self.fields.keyOrder = [
            'alias',
        ]

    def clean(self):
        """
        Check whether the user has edited the email field or not.
        If user edit the email field,
        we should check the email is present already or not.
        Otherwise we can allow the data to update.
        """
        cleaned_data = super(EditProfileForm, self).clean()
        return cleaned_data


class ProfilePasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        length_of_old_password = len(str(old_password))
        if length_of_old_password > 4:
            raise forms.ValidationError(u'Please enter a valid old password')
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        length_of_new_password = len(str(new_password))
        if length_of_new_password > 4:
            raise forms.ValidationError(u'New password should be \
             maximum of 4 characters')
        return new_password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        length_of_confirm_password = len(str(confirm_password))
        if length_of_confirm_password > 4:
            raise forms.ValidationError(u'Confirm new password should be \
             maximum of 4 characters')
        return confirm_password

    def clean(self):
        try:
            if self.cleaned_data['new_password'] != \
                    self.cleaned_data['confirm_password']:
                raise forms.ValidationError(_('New passwords does not match'))
            else:
                return self.cleaned_data
        except KeyError:
            raise forms.ValidationError(_('Plase enter passwords \
             in a valid format'))
