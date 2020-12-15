from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    #get the list
    def get_queryset( self ):
        ''' Return the last five published questions '''
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset( self ):
        '''
        Exclude any questions that aren't published yet
        '''
        # the = here is the same as the SQL <=
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote( request, pk ):
    # dealing with the form 
    # taking the value passed from request 
    question = get_object_or_404(Question, pk=pk) ## using a shortcut to deal with 404
    try:
        selected_choice = question.choice_set.get(pk= request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        # render ( request, template, dictionary )
        return render( request, 'polls/detail.html', {"question": question, 'error_message':"You didn't select a choice"} )
    else:
        selected_choice.votes += 1 
        selected_choice.save()

        # an HttpResponseRedirect must be given back after successfully dealing 
        # with the post data. This prevents data from being posted twice if a 
        # user hits the Back Button
        return HttpResponseRedirect( reverse('polls:results', args=(question.id, )) )
