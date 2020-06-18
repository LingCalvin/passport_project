from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from django.core.exceptions import ValidationError


class Workforce(models.Model):
    workforce = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.workforce

def validate_performance(value):
    if value < 1 or value > 10:
        raise ValidationError(f'{value} is not between 1 and 10 inclusive')


PERFORMANCE_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]
class Contract(models.Model):
    client = models.ForeignKey(Student, on_delete=models.CASCADE)
    workforce = models.ForeignKey(Workforce, null=True, on_delete=models.CASCADE)
    end_date = models.DateTimeField()
    performance = models.IntegerField(null=True, blank=True, choices=PERFORMANCE_CHOICES)

    def __str__(self):
        return f'{self.client} - {self.workforce} - {self.end_date}'


class WIAWDP(models.Model):
    career_pathway = models.CharField(max_length=200)
    cip_code = models.CharField(max_length=7)
    program_title = models.CharField(max_length=200)
    date_approved = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.program_title} - {self.location} ({self.cip_code})'
