from app.forms import RegistrationForm
from app.forms import EditProfileForm, ProfilePasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from app.models import UserProfile
# from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            dob = form.cleaned_data['date_of_birth']
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            profile = UserProfile(user=user, date_of_birth=dob)
            profile.save()
            return HttpResponseRedirect('/')
        return render(request, 'registration/register.html', {'form': form})
    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def register_success(request):
    return HttpResponseRedirect(reverse('home_page'))


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))


@login_required
def home(request):
    return HttpResponseRedirect('/')


class MyProfileView(TemplateView):
    """
    Enables viewing of the user's profile in the HTML site, by the profile
    owner.
    """
    template_name = 'app/viewprofile.html'

    def get_context_data(self, **kwargs):
        """ Retrieve the user profile
        """
        context = super(MyProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile
        context['username'] = user.username

        if profile.alias:
            context['alias'] = profile.alias
        else:
            context['alias'] = 'Anonymous'

        context['date_of_birth'] = profile.date_of_birth
        return context


class MyProfileEdit(FormView):
    """
    Enables editing of the user's profile in the HTML site
    """
    form_class = EditProfileForm
    template_name = 'app/editprofile.html'

    def get_initial(self):
        initial = self.initial.copy()
        user = self.request.user
        profile = user.profile
        initial['username'] = user.username

        if profile.alias:
            initial['alias'] = profile.alias
        else:
            initial['alias'] = 'Anonymous'

        initial['date_of_birth'] = profile.date_of_birth
        return initial

    def form_valid(self, form):
        user = self.request.user
        profile = user.profile
        profile.alias = form.cleaned_data['alias']
        profile.save()
        return HttpResponseRedirect(reverse('view_my_profile'))


class ProfilePasswordChangeView(FormView):
    form_class = ProfilePasswordChangeForm
    template_name = 'app/change_password.html'

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return HttpResponseRedirect(reverse('view_my_profile'))
        messages.error(
            self.request,
            _('The Old password is incorrect.')
        )
        return render(self.request, 'app/change_password.html', {'form': form})