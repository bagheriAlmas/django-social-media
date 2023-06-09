from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.urls import reverse

from profiles.utils import get_random_code


class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_available_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])  # remove duplicate value automatically
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
                print(qs)
        print(accepted)
        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=200, blank=True, default='No Bio...')
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} ({self.created_at.strftime("%Y-%m-%d")})'

    def get_absolute_url(self):
        return reverse('profiles-detail-view', kwargs={'slug': self.slug})

    __init_first_name = None
    __init_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_first_name = self.first_name
        self.__init_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__init_first_name or self.last_name != self.__init_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts_count(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_count(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'like':
                total_liked += 1
        return total_liked

    def get_likes_received_count(self):
        posts = self.posts.all()
        print(self.posts.all().count())
        total_liked = 0
        for item in posts:
            print(item.like_set)
            print(item.liked.all())
            total_liked += item.like_set.all().count()
        return total_liked


STATUS_CHOICES = (
    ('send', 'Send'),
    ('accepted', 'Accepted')
)


class RelationshipManager(models.Manager):
    def invitation_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
