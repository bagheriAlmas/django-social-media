from django.shortcuts import render, redirect

from posts.models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm


def post_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_added = False

    if 'btnPostSubmit' in request.POST:
        print(request.POST)
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_added = True
    if 'btnCommentSubmit' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentModelForm()

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,

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
