from django.shortcuts import render
from .models import Profile, Relationship
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
