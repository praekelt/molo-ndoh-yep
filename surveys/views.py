from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from surveys.models import Answer, Survey


class IndexView(generic.ListView):
    template_name = 'surveys/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Survey.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'


def survey(request, question_id):
    question = get_object_or_404(Survey, pk=question_id)
    try:
        answer = request.POST['answer']
        question.answer.answer_text = "testing"
        question.answer.save()
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'surveys/detail.html', {
            'question': question,
            'error_message': "You didn't enter the answer.",
        })
    else:
        return HttpResponseRedirect(reverse('home_page'))
