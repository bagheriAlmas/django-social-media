from django.urls import path
from .views import (profile_view, invites_received_view, suggestions_list_view, ProfileListView,
                    send_invitation_view, remove_from_friends_view, accept_invitation, reject_invitation,
                    ProfileDetailView, pending_request_view)

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', profile_view, name='my-profile-view'),
    path('suggestion-list/', suggestions_list_view, name='suggestion-list-view'),
    path('send-invite', send_invitation_view, name='send-invite'),
    path('remove-friend', remove_from_friends_view, name='remove-friend'),
    path('myinvites/', invites_received_view, name='my-invites-view'),
    path('myinvites/accept', accept_invitation, name='accept-invites-view'),
    path('myinvites/reject', reject_invitation, name='reject-invites-view'),
    path('myinvites/pending', pending_request_view, name='pending-request-view'),
    path('<slug:slug>/', ProfileDetailView.as_view(), name='profiles-detail-view'),

]
