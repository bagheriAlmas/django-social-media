from django.urls import path
from .views import profile_view, invites_received_view

urlpatterns = [
    path('myprofile/', profile_view, name='my-profile-view'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
]
