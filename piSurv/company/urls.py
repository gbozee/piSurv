from posixpath import basename
from django.urls import path,include

from . import views
from .views import SurveyList,UserViewSet,SubmittedDataViewset,QuestionList
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()


router.register('survey',SurveyList,basename="survey"),
router.register('users',UserViewSet)
router.register('submit',SubmittedDataViewset)
router.register('question',QuestionList)


urlpatterns = [

    path('company/',include(router.urls)),
    # path(''.include(router.urls))
]