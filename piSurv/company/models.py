from array import array
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import CharField
from user.models import ProfileUser
from django.utils import timezone
import jsonfield


User = get_user_model()


class TestModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    book = models.CharField(max_length=100, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    company_logo = models.ImageField(
        upload_to="profile_images", default="blank-profile-picture.png"
    )
    company_bio = models.TextField(max_length=800, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def answers(self):
        return Choice.objects.filter(question__survey=self).all()


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE
    )  # i dont think you should tie the question to the survey.
    name_of_question = models.CharField(max_length=200)
    pub_date = models.DateField("date published", default=timezone.now)
    choices = models.JSONField(default=dict, null=True)

    def __str__(self):
        return self.name_of_question

    @property
    def choices_array(self):
        choices = self.choices or {}
        return choices.get("options") or []


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question"
    )
    text = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="individual",
        null=True,
        blank=True,
    )
    # you can tie the answer to the survey here but we would work with your original modelling

    def __str__(self):
        return f"{self.question.name_of_question}:{self.text}"


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


# Create your models here.
