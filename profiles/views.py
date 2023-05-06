from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView

from .models import Profile, Relationship, ProfileManager
from .forms import ProfileModelForm


# Create your views here.
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/myprofile.html', context)


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    invites_received = Relationship.objects.invitation_received(profile)

    context = {
        'invites_received': invites_received
    }
    return render(request, 'profiles/my-invites.html', context)


# def profile_list_view(request):
#     user = request.user
#     qs = Profile.objects.get_all_profiles(user)
#
#     context = {
#         'qs': qs
#     }
#     return render(request, 'profiles/profile-list.html', context)
#

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile-list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)

        relationship_receiver_object = Relationship.objects.filter(sender=profile)
        relationship_sender_object = Relationship.objects.filter(receiver=profile)

        relationship_receiver_list = []
        relationship_sender_list = []

        for item in relationship_receiver_object:
            relationship_receiver_list.append(item.receiver.user)
        for item in relationship_sender_object:
            relationship_sender_list.append(item.sender.user)

        context['relationship_receiver'] = relationship_receiver_list
        context['relationship_sender'] = relationship_sender_list
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


def available_profile_list_view(request):
    user = request.user
    available_profiles = Profile.objects.get_all_available_profiles_to_invite(user)

    context = {
        'available_profiles': available_profiles
    }
    return render(request, 'profiles/available-profile-list.html', context)
