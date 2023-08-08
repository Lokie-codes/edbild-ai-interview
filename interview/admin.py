from django.contrib import admin
from .models import Interview, Question, Answer, Score, Feedback, Candidate

# Register your models here.
admin.site.register(Interview)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Score)
admin.site.register(Feedback)
admin.site.register(Candidate)
