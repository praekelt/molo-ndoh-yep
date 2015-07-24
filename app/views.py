from app.forms import RegistrationForm
from app.forms import EditProfileForm, ProfilePasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from app.models import UserProfile
import datetime
# from django import forms
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
# from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                date = datetime.datetime(
                    year=int(form.cleaned_data['year']),
                    month=int(form.cleaned_data['month']),
                    day=int(form.cleaned_data['day'])
                )
                dob = date.strftime('%Y-%m-%d')
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                )
                profile = UserProfile(user=user, date_of_birth=dob)
                profile.save()
                return HttpResponseRedirect('/')
            except ValueError:
                messages.error(request, 'The day is out of range for month.')
        variables = RequestContext(request, {
            'form': form
        })
        return render_to_response(
            'registration/register.html',
            variables,
        )
    form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return HttpResponseRedirect('/')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


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

    def get_form(self, form_class):
        form = super(MyProfileEdit, self).get_form(form_class)
        return form

    def form_valid(self, form):
        user = self.request.user
        profile = user.profile
        profile.alias = form.cleaned_data['alias']
        profile.save()
        return HttpResponseRedirect(reverse('view_my_profile'))


class ProfilePasswordChangeView(FormView):
    form_class = ProfilePasswordChangeForm
    template_name = 'app/change_password.html'

    def get_form(self, form_class):
        form = super(ProfilePasswordChangeView, self).get_form(form_class)
        return form

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return HttpResponseRedirect(reverse('view_my_profile'))
        else:
            messages.error(
                self.request,
                'The Old password is incorrect.'
            )
            variables = RequestContext(
                self.request,
                {'form': form}
            )
            return render_to_response(
                'app/change_password.html',
                variables,
            )
        variables = RequestContext(self.request, {'form': form})
        return render_to_response(
            'app/change_password.html',
            variables,
        )
