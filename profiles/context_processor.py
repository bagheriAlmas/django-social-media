from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'picture': profile.avatar}
    return {}


def invitation_receive_number(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        post_count = Relationship.objects.invitation_received(profile)
        return {'invites_num': post_count}
    return {}
