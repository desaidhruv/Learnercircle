from django.db import models
from django.urls import reverse

# Create your models here.
class Competition(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    scheduled_date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    rules = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("student:competitionDetails", kwargs={"pk": self.pk})
    
class CompetitionRegistration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    dob = models.DateField()
    phone = models.CharField(max_length=20)
