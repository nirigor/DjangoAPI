from django.db import models

class Participants(models.Model):
    # General
    ParticipantId = models.AutoField(primary_key=True)
    SurveyStartTs = models.DateTimeField()
    SurveyEndTs = models.DateTimeField()
    TQ1 = models.BooleanField()
    TQ2 = models.BooleanField()
    ProlificId = models.CharField(max_length=100)
    Token = models.CharField(max_length=255)

    # Gender
    GENDER_OPTIONS = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("E", "External")
    ]
    Gender = models.CharField(max_length=1, choices=GENDER_OPTIONS)

    # Age
    AGE_OPTIONS = [
        ("0", "External"),
        ("1", "18 - 29"),
        ("2", "30 - 39"),
        ("3", "40 - 49"),
        ("4", "50 - 59"),
        ("5", "60 +")
    ]
    Age = models.CharField(max_length=1, choices=AGE_OPTIONS)

    # Demographics
    MARITAL_STATUS_OPTIONS = [
        ("SI", "Single"),
        ("MA", "Married"),
        ("SE", "Separated"),
        ("DI", "Divorced"),
        ("WI", "Widowed")
    ]
    MaritalStatus = models.CharField(max_length=2, choices=MARITAL_STATUS_OPTIONS)
    
    NumberOfChildren = models.PositiveSmallIntegerField()
    NumberOfYoungChildren = models.PositiveSmallIntegerField()
    Minority = models.BooleanField()
    
    DEBTS_OPTIONS = [
        ("0", "No Debts"),
        ("1", "Some Debts"),
        ("2", "A lot")
    ]
    Debts = models.CharField(max_length=1, choices=DEBTS_OPTIONS)
    
    INCOME_LEVEL_OPTIONS = [
        ("0", "Below Average"),
        ("1", "Average"),
        ("2", "Above Average")
    ]
    Income = models.CharField(max_length=1, choices=INCOME_LEVEL_OPTIONS)
    
    EDUCATION_OPTIONS = [
        ("ES", "Elementary School or below"),
        ("HS", "High School"),
        ("BA", "Bachelor's Degree"),
        ("MA", "Master's Degree"),
        ("DR", "Doctorate")
    ]
    Education = models.CharField(max_length=2, choices=EDUCATION_OPTIONS)
    
    LEGAL_KNOWLEDGE_OPTIONS = [
        ("0", "No Knowledge"),
        ("1", "Some Knowledge"),
        ("2", "Degree in law")
    ]
    LegalKnowledge = models.CharField(max_length=1, choices=LEGAL_KNOWLEDGE_OPTIONS)
    
    InvolvedInLegalDispute = models.BooleanField()

    ExperienceWithCourtProceedings = models.BooleanField()
    CourtProceedingsSatisfaction = models.PositiveSmallIntegerField(default=0)
    ExperienceWithCourtProceedingsText = models.TextField(blank=True)

    ExperienceWithMediation = models.BooleanField()
    MediationSatisfaction = models.PositiveSmallIntegerField(default=0)
    ExperienceWithMediationText = models.TextField(blank=True)

    ExperienceWithArbitration = models.BooleanField()
    ArbitrationSatisfaction = models.PositiveSmallIntegerField(default=0)
    ExperienceWithArbitrationText = models.TextField(blank=True)

    Country = models.CharField(max_length=50, default="Unknown")

    # Big Five
    BF1 = models.PositiveSmallIntegerField()
    BF2 = models.PositiveSmallIntegerField()
    BF3 = models.PositiveSmallIntegerField()
    BF4 = models.PositiveSmallIntegerField()
    BF5 = models.PositiveSmallIntegerField()
    BF6 = models.PositiveSmallIntegerField()
    BF7 = models.PositiveSmallIntegerField()
    BF8 = models.PositiveSmallIntegerField()
    BF9 = models.PositiveSmallIntegerField()
    BF10 = models.PositiveSmallIntegerField()
    BF11 = models.PositiveSmallIntegerField()
    BF12 = models.PositiveSmallIntegerField()
    BF13 = models.PositiveSmallIntegerField()
    BF14 = models.PositiveSmallIntegerField()
    BF15 = models.PositiveSmallIntegerField()

    BFOpennessScore = models.FloatField()
    BFAgreeablenessScore = models.FloatField()
    BFExtraversionScore = models.FloatField()
    BFConscientiousnessScore = models.FloatField()
    BFNeuroticismScore = models.FloatField()

    #Thomas Killman
    TK1 = models.CharField(max_length=1)
    TK2 = models.CharField(max_length=1)
    TK3 = models.CharField(max_length=1)
    TK4 = models.CharField(max_length=1)
    TK5 = models.CharField(max_length=1)
    TK6 = models.CharField(max_length=1)
    TK7 = models.CharField(max_length=1)
    TK8 = models.CharField(max_length=1)
    TK9 = models.CharField(max_length=1)
    TK10 = models.CharField(max_length=1)

    TKAccommodatingScore = models.PositiveSmallIntegerField()
    TKCompetingScore = models.PositiveSmallIntegerField()
    TKAvoidingScore = models.PositiveSmallIntegerField()
    TKCompromisingScore = models.PositiveSmallIntegerField()
    TKCollaboratingScore = models.PositiveSmallIntegerField()

    # Stories

    DISPUTE_OPTIONS = [
        ("MC", "Major Conflict"),
        ("SD", "Serious Dispute"),
        ("CD", "Common Dispute"),
        ("MU", "Misunderstanding"),
        ("MD", "Minor Disagreement")
    ]

    STRENGTH_OPTIONS = [
        ("ST", "Stronger"),
        ("WE", "Weaker")
    ]

    SELECTION_OPTIONS = [
        ("AD", "Adjudication"),
        ("AR", "Arbitration"),
        ("ME", "Mediation"),
        ("NE", "Negotiation"),
        ("LG", "Let go"),
        ("PC", "Public Complaint")
    ]

    # Story 1
    ST1Number = models.PositiveSmallIntegerField()
    ST1Feelings = models.TextField(blank=False)

    ST1Speed = models.PositiveSmallIntegerField()
    ST1Privacy = models.PositiveSmallIntegerField()
    ST1PublicVindication = models.PositiveSmallIntegerField()
    ST1NeutralOpinion = models.PositiveSmallIntegerField()
    ST1MinimizeCosts = models.PositiveSmallIntegerField()
    ST1MaintainImproveRelationship = models.PositiveSmallIntegerField()
    ST1CreatePrecedent = models.PositiveSmallIntegerField()
    ST1MinMaxCompensation = models.PositiveSmallIntegerField()
    ST1CreativeSolution = models.PositiveSmallIntegerField()
    ST1ControlOfProcess = models.PositiveSmallIntegerField()
    ST1ControlOfOutcome = models.PositiveSmallIntegerField()
    ST1ShiftResponsibility = models.PositiveSmallIntegerField()
    ST1EnsuringCompliance = models.PositiveSmallIntegerField()
    ST1TransformationOfTheParties = models.PositiveSmallIntegerField()
    ST1ImproveUnderstanding = models.PositiveSmallIntegerField()
    ST1RecognitionApology = models.PositiveSmallIntegerField()

    ST1Classification = models.CharField(max_length=2, choices=DISPUTE_OPTIONS)
    ST1StrengthPosition = models.CharField(max_length=2, choices=STRENGTH_OPTIONS)
    ST1Selection = models.CharField(max_length=2, choices=SELECTION_OPTIONS)
    ST1SelectionText = models.TextField(blank=True)

    # Story 2
    ST2Number = models.PositiveSmallIntegerField()
    ST2Feelings = models.TextField(blank=False)

    ST2Speed = models.PositiveSmallIntegerField()
    ST2Privacy = models.PositiveSmallIntegerField()
    ST2PublicVindication = models.PositiveSmallIntegerField()
    ST2NeutralOpinion = models.PositiveSmallIntegerField()
    ST2MinimizeCosts = models.PositiveSmallIntegerField()
    ST2MaintainImproveRelationship = models.PositiveSmallIntegerField()
    ST2CreatePrecedent = models.PositiveSmallIntegerField()
    ST2MinMaxCompensation = models.PositiveSmallIntegerField()
    ST2CreativeSolution = models.PositiveSmallIntegerField()
    ST2ControlOfProcess = models.PositiveSmallIntegerField()
    ST2ControlOfOutcome = models.PositiveSmallIntegerField()
    ST2ShiftResponsibility = models.PositiveSmallIntegerField()
    ST2EnsuringCompliance = models.PositiveSmallIntegerField()
    ST2TransformationOfTheParties = models.PositiveSmallIntegerField()
    ST2ImproveUnderstanding = models.PositiveSmallIntegerField()
    ST2RecognitionApology = models.PositiveSmallIntegerField()

    ST2Classification = models.CharField(max_length=2, choices=DISPUTE_OPTIONS)
    ST2StrengthPosition = models.CharField(max_length=2, choices=STRENGTH_OPTIONS)
    ST2Selection = models.CharField(max_length=2, choices=SELECTION_OPTIONS)
    ST2SelectionText = models.TextField(blank=True)

    # Story 3
    ST3Number = models.PositiveSmallIntegerField(default=99)
    ST3Feelings = models.TextField(blank=False, default="[]")

    ST3Speed = models.PositiveSmallIntegerField(default=99)
    ST3Privacy = models.PositiveSmallIntegerField(default=99)
    ST3PublicVindication = models.PositiveSmallIntegerField(default=99)
    ST3NeutralOpinion = models.PositiveSmallIntegerField(default=99)
    ST3MinimizeCosts = models.PositiveSmallIntegerField(default=99)
    ST3MaintainImproveRelationship = models.PositiveSmallIntegerField(default=99)
    ST3CreatePrecedent = models.PositiveSmallIntegerField(default=99)
    ST3MinMaxCompensation = models.PositiveSmallIntegerField(default=99)
    ST3CreativeSolution = models.PositiveSmallIntegerField(default=99)
    ST3ControlOfProcess = models.PositiveSmallIntegerField(default=99)
    ST3ControlOfOutcome = models.PositiveSmallIntegerField(default=99)
    ST3ShiftResponsibility = models.PositiveSmallIntegerField(default=99)
    ST3EnsuringCompliance = models.PositiveSmallIntegerField(default=99)
    ST3TransformationOfTheParties = models.PositiveSmallIntegerField(default=99)
    ST3ImproveUnderstanding = models.PositiveSmallIntegerField(default=99)
    ST3RecognitionApology = models.PositiveSmallIntegerField(default=99)

    ST3Classification = models.CharField(max_length=2, choices=DISPUTE_OPTIONS, default="XX")
    ST3StrengthPosition = models.CharField(max_length=2, choices=STRENGTH_OPTIONS, default="XX")
    ST3Selection = models.CharField(max_length=2, choices=SELECTION_OPTIONS, default="XX")
    ST3SelectionText = models.TextField(blank=True)