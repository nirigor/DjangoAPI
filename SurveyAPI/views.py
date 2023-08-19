from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from SurveyAPI.models import Participants 
from SurveyAPI.serializers import ParticipantSerializer

import hashlib
import statistics
from dateutil import parser

MIN_DURATION = 60 * 8

def attention_check(data):
    ts1 = parser.parse(data['SurveyStartTs'])
    ts2 = parser.parse(data['SurveyEndTs'])
    if ((ts2 - ts1).total_seconds() < MIN_DURATION):
        return False
    if (data['TQ1'] == "true" or data['TQ2'] == "true"):
        return False
    return True

def generate_token(data):
    SALT = 'MDMAAESKLYN'
    string_to_encode = SALT + data['ProlificId'] + data['SurveyStartTs'] + data['SurveyEndTs']
    token = hashlib.md5(string_to_encode.encode('UTF-8')).hexdigest()
    return token


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getData(request):
    id = int(request.GET['id']) if 'id' in request.GET.keys() else 0
    if(id):
        participant = Participants.objects.get(ParticipantId=id)
        participant_serializer = ParticipantSerializer(participant, many=False)
    else:
        participants = Participants.objects.all()
        participant_serializer = ParticipantSerializer(participants, many=True)
    return JsonResponse(participant_serializer.data, safe=False)

@csrf_exempt
@api_view(['POST'])
def participantApi(request):
    try:
        data = JSONParser().parse(request)

        if (data['ProlificId'] != 'unpaid' and len(Participants.objects.all().filter(ProlificId=data['ProlificId']))):
            return JsonResponse(status=401, data={'message' : 'Participation in this survey is limited to one attempt.'}, safe=False)

        # Calculate BFI-S Score
        # https://www.psytoolkit.org/survey-library/big5-bfi-s.html

        data['BFOpennessScore'] = statistics.mean([int(data['BF7']), int(data['BF8']), int(data['BF9'])])
        data['BFAgreeablenessScore'] = statistics.mean([int(data['BF10']), int(data['BF11']), int(data['BF12'])])
        data['BFExtraversionScore'] = statistics.mean([int(data['BF4']), int(data['BF5']), int(data['BF6'])])
        data['BFConscientiousnessScore'] = statistics.mean([int(data['BF13']), int(data['BF14']), int(data['BF15'])])
        data['BFNeuroticismScore'] = statistics.mean([int(data['BF1']), int(data['BF2']), int(data['BF3'])])

        # Calculate TKI
        data['TKAccommodatingScore'] = (data['TK2'] == 'B') + (data['TK3'] == 'B') + (data['TK7'] == 'B') + (data['TK10'] == 'A')
        data['TKCompetingScore'] = (data['TK2'] == 'A') + (data['TK5'] == 'B') + (data['TK6'] == 'A') + (data['TK9'] == 'B')
        data['TKAvoidingScore'] = (data['TK4'] == 'B') + (data['TK5'] == 'A') + (data['TK8'] == 'A') + (data['TK10'] == 'B')
        data['TKCompromisingScore'] = (data['TK1'] == 'A') + (data['TK3'] == 'A') + (data['TK8'] == 'B') + (data['TK9'] == 'A')
        data['TKCollaboratingScore'] = (data['TK1'] == 'B') + (data['TK4'] == 'A') + (data['TK6'] == 'B') + (data['TK7'] == 'A')
        
        feedback = {
            'BFOpennessScore' : data['BFOpennessScore'],
            'BFAgreeablenessScore' : data['BFAgreeablenessScore'],
            'BFExtraversionScore' : data['BFExtraversionScore'],
            'BFConscientiousnessScore' : data['BFConscientiousnessScore'],
            'BFNeuroticismScore' : data['BFNeuroticismScore'],
            'TKAccommodatingScore' : data['TKAccommodatingScore'],
            'TKCompetingScore' : data['TKCompetingScore'],
            'TKAvoidingScore' : data['TKAvoidingScore'],
            'TKCompromisingScore' : data['TKCompromisingScore'],
            'TKCollaboratingScore' : data['TKCollaboratingScore']
        }

        if attention_check(data):
            data['Token'] = generate_token(data)
            feedback['Vaid'] = True
            feedback['Message'] = 'You have successfully completed the survey.'
            status_code = 200
        else:
            data['Token'] = 'Attention Validation has failed.'
            feedback['Valid'] = False
            feedback['Message'] = 'Attention verification failed.'
            status_code = 451
        feedback['Token'] = data['Token']

        participant_serializer = ParticipantSerializer(data=data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            return JsonResponse(status=status_code, data=feedback, safe=False)
        return JsonResponse(status=400, data={'message' : participant_serializer.errors}, safe=False)
    except Exception as e:
        return JsonResponse(status=500, data={'message' : 'A server side error has occured.'}, safe=False)
