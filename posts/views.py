from django.shortcuts import render

from posts.models import Post


def post_list_view(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }

    return render(request, 'posts/post-list.html', context)
