from django.shortcuts import render
from .models import Profile


# Create your views here.
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'user': profile,
    }
    return render(request, 'profiles/myprofile.html', context)
