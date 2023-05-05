from django.shortcuts import render, redirect

from posts.models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm


def post_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    form = PostModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = profile
        instance.save()
        form = PostModelForm()

    context = {
        'posts': posts,
        'profile': profile,
        'form': form,
    }
    return render(request, 'posts/post-list.html', context)


def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, create = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not create:
            if like.value == 'like':
                like.value = 'unlike'
            else:
                like.value = 'like'
        else:
            like.value = 'like'

            post_obj.save()
            like.save()
    return redirect('post-list')
