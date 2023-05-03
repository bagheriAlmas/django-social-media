from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm


# Create your views here.
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'profiles/myprofile.html', context)
