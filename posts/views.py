import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from posts.models import Post, Like
from profiles.models import Profile, Relationship
from .forms import PostModelForm, CommentModelForm, ImageForm


@login_required
def post_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    user = request.user
    suggestions = Profile.objects.get_all_available_profiles_to_invite(user)
    random.shuffle(suggestions)

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

    # ---------------------------------

    relationship_receiver_object = Relationship.objects.filter(sender=profile)
    relationship_sender_object = Relationship.objects.filter(receiver=profile)

    relationship_receiver_list = []
    relationship_sender_list = []

    for item in relationship_receiver_object:
        relationship_receiver_list.append(item.receiver.user)
    for item in relationship_sender_object:
        relationship_sender_list.append(item.sender.user)

    # ---------------------------------

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,
        'suggestions': suggestions[:5],
        'relationship_receiver': relationship_receiver_list,
        'relationship_sender': relationship_sender_list,
    }
    return render(request, 'posts/post-list.html', context)


@login_required
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

        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }
        # return JsonResponse(data, safe=False)
    return redirect('post-list')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete this post')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update this post")
            return super().form_valid(form)


def index(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    profile = Profile.objects.get(user=request.user)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = profile
        instance.save()
        return JsonResponse({'message': 'works'})
    context = {
        'form': form
    }
    return render(request, 'test/test.html', context)
