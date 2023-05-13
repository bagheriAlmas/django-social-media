from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Profile, Relationship, ProfileManager
from .forms import ProfileModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
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


@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    invites_received = Relationship.objects.invitation_received(profile)
    is_empty = False
    if len(invites_received.all()) == 0:
        is_empty = True
    context = {
        'invites_received': invites_received,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my-invites.html', context)


# def profile_list_view(request):
#     user = request.user
#     qs = Profile.objects.get_all_profiles(user)
#
#     context = {
#         'qs': qs
#     }
#     return render(request, 'profiles/profile-list.html', context)
#

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile-list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)

        relationship_receiver_object = Relationship.objects.filter(sender=profile)
        relationship_sender_object = Relationship.objects.filter(receiver=profile)

        relationship_receiver_list = []
        relationship_sender_list = []

        for item in relationship_receiver_object:
            relationship_receiver_list.append(item.receiver.user)
        for item in relationship_sender_object:
            relationship_sender_list.append(item.sender.user)

        context['relationship_receiver'] = relationship_receiver_list
        context['relationship_sender'] = relationship_sender_list
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self, queryset=None):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)

        relationship_receiver_object = Relationship.objects.filter(sender=profile)
        relationship_sender_object = Relationship.objects.filter(receiver=profile)

        relationship_receiver_list = []
        relationship_sender_list = []

        for item in relationship_receiver_object:
            relationship_receiver_list.append(item.receiver.user)
        for item in relationship_sender_object:
            relationship_sender_list.append(item.sender.user)

        context['relationship_receiver'] = relationship_receiver_list
        context['relationship_sender'] = relationship_sender_list
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


@login_required
def send_invitation_view(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')


@login_required
def remove_from_friends_view(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relationship = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')


@login_required
def suggestions_list_view(request):
    user = request.user
    suggestions = Profile.objects.get_all_available_profiles_to_invite(user)

    context = {
        'suggestions': suggestions
    }
    return render(request, 'profiles/available-profile-list.html', context)


@login_required
def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relationship.status == 'send':
            relationship.status = 'accepted'
            relationship.save()
    return redirect('my-invites-view')


@login_required
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relationship.delete()
    return redirect('my-invites-view')
