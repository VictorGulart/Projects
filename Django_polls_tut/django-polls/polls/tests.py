import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

# Create your tests here.

##### AUTOMATE THE CREATION OF A QUESTION #####
def create_question(question_text, days):
    '''
    Create a question with the given text and published the given
    number of days 'ofset' to now() (negative for questions published
    in the past, positive for questions that have yer to be published.)
    '''
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_date=time)

##### TESTING THE INDEX VIEW #####
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        '''
        If no question exist, an appropriate message is displayd
        '''
        response = self.client.get(reverse( 'polls:index' ))
        self.assertEqual( response.status_code, 200 )
        self.assertContains( response, 'No polls are available.' ) # check where is this
        self.assertQuerysetEqual( response.context['latest_question_list'], [])

    def test_past_question( self ):
        '''
        Questions with a pub_date in the past are displayed on the index page
        '''
        create_question(question_text='Past Question.', days=-30)
        response = self.client.get( reverse( 'polls:index' ) )
        self.assertQuerysetEqual( 
                response.context['latest_question_list'], 
                ['<Question: Past Question.>'] )

    def test_future_quesion( self ):
        '''
        Question with a pub_date in the future aren't displayed 
        on the index page.
        '''
        create_question(question_text='Future Question.', days=30)
        response = self.client.get( reverse( 'polls:index' ) ) # get the website like a user
        self.assertContains( response, 'No polls are available.' ) # get no question
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    
    def test_future_question_and_past_question( self ):
        '''
        Even if both past and future question exist, only past question
        are displayed.
        '''
        create_question(question_text='Past Question.', days=-30)
        create_question(question_text='Future Question.', days=30)
        response = self.client.get( reverse( 'polls:index' ) ) # get the website like a user
        self.assertQuerysetEqual( 
                response.context['latest_question_list'], 
                ['<Question: Past Question.>']
        )

    def test_two_past_questions( self ):
        create_question(question_text='Past Question 1.', days=-30)
        create_question(question_text='Past Question 2.', days=-5)
        response = self.client.get( reverse( 'polls:index' ) ) # get the website like a user
        self.assertQuerysetEqual( 
                response.context['latest_question_list'], 
                ['<Question: Past Question 2.>', '<Question: Past Question 1.>']
        )

##### TESTING DETAIL VIEW FOR USERS #####
class QuestionDetailViewTests(TestCase):
    def test_future_question( self ):
        '''
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        '''
        future_question = create_question(question_text='Future Question.', days=5)
        url = reverse( 'polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual( response.status_code, 404 )

    def test_past_question( self ):
        '''
        The detail view of a question with a pub_date in the past
        displays the question's text.
        '''
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse( 'polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains( response, past_question.question_text )





##### TESTING THE INTERNAL BEHAVIOUR OF THE CODE #####
class QuestionModelTests(TestCase):
    def test_was_pub_recently_with_future_question(self):
        '''
            was_pub_recently() returns False for questions whose
            pub_date is in the future
        '''

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_pub_recently(), False)
    
    def test_was_pub_recently_with_old_question( self ):
        '''
            was_pub_recently() return False for questions whose
            pub_date is older than 1 day
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_pub_recently(), False)

    def test_was_pub_recently_with_recent_question( self ):
        '''
            was_pub_recently() return True for questions whose
            pub_date is within the last day
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_pub_recently(), True)

