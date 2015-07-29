# import re
from django import forms
# from PIL import Image
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from django.core.exceptions import ValidationError
import datetime
from django.forms.extras.widgets import SelectDateWidget


class RegistrationForm(forms.Form):
    this_year = datetime.date.today().year
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        widget=forms.TextInput(
            attrs=dict(required=True, max_length=30)
        ),
        label=_("Username"),
        error_messages={'invalid': _("This value must contain only letters, \
         numbers and underscores.")})
    password = forms.RegexField(
        regex=r'^\d{4}$',
        widget=forms.PasswordInput(
            attrs=dict(
                required=True,
                max_length=4,
                render_value=False,
                type='password'
            )
        ),
        label=_("PIN")
    )

    date_of_birth = forms.DateField(
        widget=SelectDateWidget(
            years=[y for y in range(1930, this_year)]
        )
    )

    def clean_username(self):
        if User.objects.filter(
            username__iexact=self.cleaned_data['username']
        ).exists():
            raise forms.ValidationError(_("Username is already exists."))
        return self.cleaned_data['username']

    def clean_date_of_birth(self):
        return self.cleaned_data['date_of_birth']

    def clean(self):
        return self.cleaned_data


class EditProfileForm(RegistrationForm):
    alias = forms.CharField(
        label=_("Display Name"),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        del self.fields['username']
        del self.fields['date_of_birth']
        self.fields.keyOrder = [
            'alias',
        ]


class ProfilePasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=4,
        min_length=4
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=4,
        min_length=4
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=4,
        min_length=4
    )

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
