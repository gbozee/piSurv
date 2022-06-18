from rest_framework import serializers
from .models import Profile,Question,TestModel,Survey

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user","company_name","company_img"]


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ["name","book"]

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id",]

class SurveySerializer(serializers.ModelSerializer):
    # question_set = serializers.PrimaryKeyRelatedField(many=True, read_only =True)
    question_set = QuestionsSerializer(many=True)
    class Meta:
        model = Survey
        fields = ["id","title","question_set"]

    
