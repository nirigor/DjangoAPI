from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from SurveyAPI.models import Participants 
from SurveyAPI.serializers import ParticipantSerializer

import hashlib
import statistics
from dateutil import parser

MIN_DURATION = 10

def attention_check(data):
    ts1 = parser.parse(data['SurveyStartTs'])
    ts2 = parser.parse(data['SurveyEndTs'])    
    if ((ts2 - ts1).total_seconds() < MIN_DURATION):
        return False
    if (data['TQ1'] or data['TQ2']):
        return False
    return True

def generate_token(data):
    SALT = 'MDMAAESKLYN'
    string_to_encode = SALT + data['ProlificId'] + data['SurveyStartTs'] + data['SurveyEndTs']
    token = hashlib.md5(string_to_encode.encode('UTF-8')).hexdigest()
    return token

@csrf_exempt
def participantApi(request):
    if request.method =='GET':
        id = int(request.GET['id']) if 'id' in request.GET.keys() else 0
        if(id):
            participant = Participants.objects.get(ParticipantId=id)
            participant_serializer = ParticipantSerializer(participant, many=False)
        else:
            participants = Participants.objects.all()
            participant_serializer = ParticipantSerializer(participants, many=True)
        return JsonResponse(participant_serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        
        if (data['ProlificId'] != 'unpaid' and len(Participants.objects.all().filter(ProlificId=data['ProlificId']))):
            return JsonResponse(status=400, data={'message' : 'ERROR: Participation in this survey is limited to one attempt.'}, safe=False)

        # Calculate BFI-S Score
        # https://www.psytoolkit.org/survey-library/big5-bfi-s.html
        
        data['BFOpennessScore'] = statistics.mean([int(data['BF7']), int(data['BF8']), int(data['BF9'])])
        data['BFAgreeablenessScore'] = statistics.mean([int(data['BF10']), int(data['BF11']), int(data['BF12'])])
        data['BFExtraversionScore'] = statistics.mean([int(data['BF4']), int(data['BF5']), int(data['BF6'])])
        data['BFConscientiousnessScore'] = statistics.mean([int(data['BF13']), int(data['BF14']), int(data['BF15'])])
        data['BFNeuroticismScore'] = statistics.mean([int(data['BF1']), int(data['BF2']), int(data['BF3'])])
        
        # Calculate TKI
        data['TKAccommodatingScore'] = \
            (data['TK1'] == 'B') + (data['TK3'] == 'B') + (data['TK4'] == 'B') + (data['TK11'] == 'B') + \
            (data['TK15'] == 'A') + (data['TK16'] == 'A') + (data['TK18'] == 'A') + (data['TK21'] == 'A') + \
            (data['TK24'] == 'A') + (data['TK25'] == 'B') + (data['TK27'] == 'B') + (data['TK30'] == 'A')
        
        data['TKCompetingScore'] = \
            (data['TK3'] == 'A') + (data['TK6'] == 'B') + (data['TK8'] == 'A') + (data['TK9'] == 'B') + \
            (data['TK10'] == 'A') + (data['TK13'] == 'B') + (data['TK14'] == 'B') + (data['TK16'] == 'B') + \
            (data['TK17'] == 'A') + (data['TK22'] == 'B') + (data['TK25'] == 'A') + (data['TK28'] == 'A')
                                    
        data['TKAvoidingScore'] = \
            (data['TK1'] == 'A') + (data['TK5'] == 'B') + (data['TK6'] == 'A') + (data['TK7'] == 'A') + \
            (data['TK9'] == 'A') + (data['TK12'] == 'A') + (data['TK15'] == 'B') + (data['TK17'] == 'B') + \
            (data['TK19'] == 'B') + (data['TK23'] == 'B') + (data['TK27'] == 'A') + (data['TK29'] == 'B')
        
        data['TKCompromisingScore'] = \
            (data['TK2'] == 'A') + (data['TK4'] == 'A') + (data['TK7'] == 'B') + (data['TK10'] == 'B') + \
            (data['TK12'] == 'B') + (data['TK13'] == 'A') + (data['TK18'] == 'B') + (data['TK20'] == 'B') + \
            (data['TK22'] == 'A') + (data['TK24'] == 'B') + (data['TK26'] == 'A') + (data['TK29'] == 'A')
        
        data['TKCollaboratingScore'] = \
            (data['TK2'] == 'B') + (data['TK5'] == 'A') + (data['TK8'] == 'B') + (data['TK11'] == 'A') + \
            (data['TK14'] == 'A') + (data['TK19'] == 'A') + (data['TK20'] == 'A') + (data['TK21'] == 'B') + \
            (data['TK23'] == 'A') + (data['TK26'] == 'B') + (data['TK28'] == 'B') + (data['TK30'] == 'B')

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
            data['Token'] = 'Attention Validation has failed..'
            feedback['Valid'] = False
            feedback['Message'] = 'ERROR: Attention verification failed..'
            status_code = 451
        feedback['Token'] = data['Token']
        
        participant_serializer = ParticipantSerializer(data=data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            return JsonResponse(status=status_code, data=feedback, safe=False)
        return JsonResponse(status=400, data={'message' : participant_serializer.errors}, safe=False)