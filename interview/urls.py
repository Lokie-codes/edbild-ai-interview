from django.urls import path
from .views import InterviewView, Index, AnswerView, CandidateView

urlpatterns = [
    path("interview/", InterviewView.as_view(), name="interview"),
    path("answer/", AnswerView.as_view(), name="answer"),
    path("home/", Index.as_view(), name="index"),
    path("", CandidateView.as_view(), name="candidate"),
]
