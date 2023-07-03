from django.urls import re_path
from SurveyAPI import views

urlpatterns = [
    re_path(r'^', views.participantApi),
    re_path(r'^participants/([0-9]+)$', views.participantApi),
]