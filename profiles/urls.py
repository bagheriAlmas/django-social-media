from django.urls import path
from .views import (profile_view, invites_received_view, available_profile_list_view, ProfileListView,
                    send_invitation_view, remove_from_friends_view, accept_invitation, reject_invitation)

urlpatterns = [
    path('myprofile/', profile_view, name='my-profile-view'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
    path('profiles-list/', ProfileListView.as_view(), name='all-profiles-view'),
    path('available-profiles-list/', available_profile_list_view, name='available-profiles-view'),
    path('send-invite/', send_invitation_view, name='send-invite'),
    path('remove-friend/', remove_from_friends_view, name='remove-friend'),
    path('myinvites/accept', accept_invitation, name='accept-invites-view'),
    path('myinvites/reject', reject_invitation, name='reject-invites-view'),

]
