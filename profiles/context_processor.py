from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'picture': profile.avatar}
    return {}



