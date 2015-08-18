from app.forms import RegistrationForm
from app.forms import EditProfileForm, ProfilePasswordChangeForm
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

import django_comments

from molo.commenting.forms import MoloCommentForm


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            user.profile.date_of_birth = form.cleaned_data['date_of_birth']
            user.profile.save()
            return HttpResponseRedirect(request.site.root_page.url)
        return render(request, 'registration/register.html', {'form': form})
    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def register_success(request):
    return HttpResponseRedirect(request.site.root_page.url)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(request.site.root_page.url)


class MyProfileView(TemplateView):
    """
    Enables viewing of the user's profile in the HTML site, by the profile
    owner.
    """
    template_name = 'app/viewprofile.html'


class MyProfileEdit(FormView):
    """
    Enables editing of the user's profile in the HTML site
    """
    form_class = EditProfileForm
    template_name = 'app/editprofile.html'

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


class CommentReplyForm(TemplateView):
    form_class = MoloCommentForm
    template_name = 'comments/reply.html'

    def get(self, request, parent_id):
        comment = get_object_or_404(
            django_comments.get_model(), pk=parent_id,
            site__pk=settings.SITE_ID)
        form = MoloCommentForm(comment.content_object, initial={
            'content_type': '%s.%s' % (
                comment.content_type.app_label,
                comment.content_type.model),
            'object_pk': comment.object_pk,
        })
        return self.render_to_response({
            'form': form,
            'comment': comment,
        })


def search(request):
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.non()
    return render(request, 'search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
