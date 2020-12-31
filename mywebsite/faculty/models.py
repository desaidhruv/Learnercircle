from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

CATEGORY_CHOICES = (
    ('AC', 'Art & Craft'),
    ('FR', 'Food Recipes'),
    ('L', 'Language')
)

# Create your models here.
class ProfileSection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=255,primary_key=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phoneno = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    years = models.CharField(max_length=255)
    hobbies = models.CharField(max_length=255)
    areaofinterest = models.CharField(max_length=255)
    socialprof = models.CharField(max_length=255)
    yourself = models.CharField(max_length=255)
    keylearn = models.CharField(max_length=255)

    def __str__(self):
        return self.username



class CourseSection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    course_category = models.CharField(choices=CATEGORY_CHOICES,max_length=10,null=True)
    course_name = models.CharField(max_length=255)
    batch_count = models.IntegerField()
    course_details = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    medium = models.CharField(max_length=255)
    days = models.CharField(max_length=255)
    key_learnings = models.CharField(max_length=255)
    age_group = models.CharField(max_length=255)
    prerequisites = models.CharField(max_length=255)
    things = models.CharField(max_length=255)

    def __str__(self):
        return self.fname
    
    def get_absolute_url(self):
        return reverse("student:courseDetails", kwargs={
            'pk': self.pk
        })

    def get_category_url(self):
        return reverse("student:course_category", kwargs={
            'category': self.course_category
        })

class BankDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=255,primary_key=True)
    accountNo = models.CharField(max_length=255)
    accountType = models.CharField(max_length=255)
    ifsc = models.CharField(max_length=255)
    bankName = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)

    def __str__(self):
        return self.accountNo

class CourseOverview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=255,primary_key=True)
    courseName = models.CharField(max_length=255)
    courseSubtitle = models.CharField(max_length=255)
    duration = models.IntegerField(default=16)
    age = models.IntegerField()
    batch = models.IntegerField()
    mediumOfInstruct = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    courseReq = models.CharField(max_length=255)
    topics = models.CharField(max_length=255)
    payment = models.IntegerField()

    def __str__(self):
        return self.courseName

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=255)
    dates = models.CharField(max_length=255)

    def __str__(self):
        return self.dates