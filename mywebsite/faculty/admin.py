from django.contrib import admin
from .models import ProfileSection,CourseSection,BankDetail,CourseOverview,Schedule

# Register your models here.
admin.site.register(ProfileSection)
admin.site.register(CourseSection)
admin.site.register(BankDetail)
admin.site.register(CourseOverview)
admin.site.register(Schedule)