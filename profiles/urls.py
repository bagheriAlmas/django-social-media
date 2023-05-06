from django.urls import path
from .views import profile_view, invites_received_view, profile_list_view

urlpatterns = [
    path('myprofile/', profile_view, name='my-profile-view'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
    path('profiles-list/', profile_list_view, name='all-profiles-view'),
]
