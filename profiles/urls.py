from django.urls import path
from .views import profile_view

urlpatterns = [
    path('myprofile/', profile_view, name='my-profile')
]
