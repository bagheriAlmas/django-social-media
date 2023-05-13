from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


class Post(models.Model):
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='photos', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                              blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def likes_count(self):
        return self.liked.all().count()

    def comments_count(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created_at',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('like', 'Like'),
    ('unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.post} - {self.value}'



class Image(models.Model):
    content = models.TextField(max_length=500, null=True, blank=True)
    file = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)

    def __str__(self):
        return self.content