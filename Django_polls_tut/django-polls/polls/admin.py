from django.contrib import admin
from .models import Question, Choice

# Register your models here.
# Just registering is to simple we can add some customization


class ChoiceInLine(admin.TabularInline):
    # This is to edit how choices appear in the question page
    # StackedInLine is a good option but for such a simple choice it would be easier
    # to show the choicetext : field + votes: field in only one line to save space
    # so use TabularInLine
    model = Choice
    extra = 1 # start with 3 choices to be added 

class QuestionAdmin( admin.ModelAdmin ):
    # this edits how the question and its fields appear on the page
    # other things can be added too, like the Choices connected to the question
    ## fields = [ 'pub_date', 'question_text'] # changing the order

    # this is to edit how the change page is viewed 
    # a method can also be added here like was_pub_recently()
    # the method display can be improve inside the models class
    list_display = ('question_text', 'pub_date', 'was_pub_recently') 
    
    # this add a filter to the side bar of the page
    # because django knows it is a DateTimeField it knows which appropriate filter options to use
    list_filter = ['pub_date']
    
    # this uses a LIKE query, so limiting the number of search fields will make it easier fot the 
    # DB to do the search
    search_fields = ['question_text']

    fieldsets = [
            (None, {'fields':['question_text']}),
            ('Date Info', {'fields':['pub_date'], 'classes':['collapse']})
            ]
    inlines = [ChoiceInLine] # add the choices in the question page

admin.site.register( Question, QuestionAdmin )
# admin.site.register( Choice ) # the choices can have their on page but it makes more sense to add them to the page of the question it is connected to, hence we create a new class to show how to display them.
