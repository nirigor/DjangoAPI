from django.urls import re_path
from SurveyAPI import views

urlpatterns = [
    re_path(r'^api/participants', views.getData),
    re_path(r'^api/participants/([0-9]+)$', views.getData),
    re_path(r'^api', views.participantApi),
]