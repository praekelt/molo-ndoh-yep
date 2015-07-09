import re
from django import forms
from PIL import Image
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import time
 
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=4, render_value=False, type='number')), label=_("PIN"))
    year = forms.IntegerField(widget=forms.TextInput(attrs={'type':'number'}), label=_("Year"))
    month = forms.IntegerField(widget=forms.TextInput(attrs={'type':'number'}), label=_("Month"))
    day = forms.IntegerField(widget=forms.TextInput(attrs={'type':'number'}), label=_("Day"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
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
        if year > thisyear or length_of_year!=4 or year<1900:
            raise forms.ValidationError(u'Please enter a valid year')
        return year
    def clean_month(self):
        month = self.cleaned_data['month']
        length_of_month = len(str(month))
        if length_of_month > 2:
            raise forms.ValidationError(u'Please enter a valid month')
        return month
    def clean_day(self):
        day = self.cleaned_data['day']
        length_of_day = len(str(day))
        if length_of_day > 2:
            raise forms.ValidationError(u'Please enter a valid day')
        return day
 
    def clean(self):
        return self.cleaned_data

class EditProfileForm(RegistrationForm):
    alias = forms.CharField(
       label=_("Display Name"),
       required=False
    )
    avatar = forms.ImageField(
        label=_("Upload Picture"),
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
            'avatar',
        ]

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar')
        if not image:
            image = None

        try:
            img = Image.open(image)
            w, h = img.size
            max_width = max_height = 500
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    _('Please use an image that is smaller or equal to '
                      '500 x 500 pixels.'))
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                raise forms.ValidationError(_('Please use a JPEG or PNG image.'))
            if len(image) > (500 * 1024):
                raise forms.ValidationError(_('Image file too large ( maximum 500KB )'))
        except AttributeError:
            pass
        return image
    def clean(self):
        """
        Check whether the user has edited the email field or not. If user edit the email field, we should check the email is present already or not. Otherwise we can allow the data to update.
        """
        cleaned_data = super(EditProfileForm, self).clean()
        return cleaned_data

class ProfilePasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError(_('The new passwords must be same'))
        else:
            return self.cleaned_data