from django.urls import path
from .views import (profile_view, invites_received_view, available_profile_list_view,ProfileListView )

urlpatterns = [
    path('myprofile/', profile_view, name='my-profile-view'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
    path('profiles-list/', ProfileListView.as_view(), name='all-profiles-view'),
    path('available-profiles-list/', available_profile_list_view, name='available-profiles-view'),
]
