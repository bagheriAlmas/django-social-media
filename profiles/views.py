from django.shortcuts import render
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


def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs
    }
    return render(request, 'profiles/profile-list.html', context)


def available_profile_list_view(request):
    user = request.user
    available_profiles = Profile.objects.get_all_available_profiles_to_invite(user)

    context = {
        'available_profiles': available_profiles
    }
    return render(request, 'profiles/available-profile-list.html', context)
