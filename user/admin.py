from django.contrib import admin

from user.models import Interest, InterestCategory, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Interest)
admin.site.register(InterestCategory)