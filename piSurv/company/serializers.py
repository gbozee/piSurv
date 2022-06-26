from doctest import debug
from rest_framework import serializers
from .models import Profile,Question,TestModel,Survey,Choice
from django.contrib.auth.models import User,auth
from rest_framework.authtoken.views import Token

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user","company_name","company_img"]


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ["name","book"]

# class ChoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Choice
#         fields = ["id","text"]

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","name_of_question"]

class SurveySerializer(serializers.ModelSerializer):
    question_set = serializers.PrimaryKeyRelatedField(many=True, read_only =True)
    # question_set = QuestionsSerializer(many = True)

    class Meta:
        model = Survey
        fields = ["id","title","question_set"]

    def create(self, validated_data):
        user = validated_data.pop("user",None)
        question_set_data = validated_data.pop("question_set")
        survey  = Survey.objects.create(user=user,**validated_data)

        for question_set in question_set_data:
            Question.objects.create(survey=survey,**question_set_data[0])

        # do this instead for efficiency
        # Question.objects.bulk_create([Question(survey=survey, **x) for x in question_set_data])
        return survey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","password"]

        extra_kwargs= {'password':{
            'write_only':True,
            'required':True
        }}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['question_id','text']

class SubmittedQuestionSerializer(serializers.ModelSerializer):
    answers = ChoiceSerializer(many=True)
    class Meta:
        model = Survey
        fields = ["id","title", "answers"]

    def create(self,validated_data):
        user = validated_data.pop("user")
        choices = Choice.objects.bulk_create([Choice(user=user,**x)for x in validated_data['answers']] )
        breakpoint()
        return choices[0].question.survey
        # submitted_data  = SubmittedQuestion.objects.create(user=user,survey=survey,**validated_data)
        return submitted_data
    
