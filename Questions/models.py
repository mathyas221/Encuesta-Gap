from django.db import models
from Questions.defines import *
from django.contrib.auth.models import User
# Create your models here.

class Cont(models.Model):
    cont = models.IntegerField(default=0)

class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=3, choices=DOMINIO_CHOICE)

    def __str__(self):
        return "%s, %s" % (self.question, self.type)


class Personal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=3, choices=POSITION_CHOICE)

    def __str__(self):
        return "usuario: %s ,Cargo: %s" % (self.user, self.position)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Personal, on_delete=models.CASCADE)
    answer = models.BooleanField()

    class Meta:
        unique_together = ['question', 'user']

    def __str__(self):
        return "%s ,Answer: %s" % (self.question, self.answer)

class Analisis(models.Model):
    type = models.CharField(max_length=50)
    total_t = models.FloatField(max_length=50)
    total_f = models.FloatField(max_length=50)
    percentaje_t = models.FloatField(max_length=50)
    percentaje_f = models.FloatField(max_length=50)