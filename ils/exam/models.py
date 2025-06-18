from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Question(models.Model):
    cognitive_ability_choices = (
        ('Level_1', 'Remember and Understand'),
        ('Level_2', 'Apply and Analyze'),
        ('Level_3', 'Evaluate and Create'),
    )

    label = models.CharField(max_length=5000)
    cognitive_ability = models.CharField(
        max_length=50, choices=cognitive_ability_choices)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    is_current_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time_spent = models.DurationField()
    times_option_changed = models.PositiveIntegerField(default=0)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Response to {self.question.label}"
