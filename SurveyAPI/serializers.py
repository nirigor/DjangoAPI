from rest_framework import serializers
from SurveyAPI.models import Participants

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = '__all__'