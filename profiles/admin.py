from django.contrib import admin
from .models import Profile, Relationship


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    filter_horizontal = ['friends']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)
