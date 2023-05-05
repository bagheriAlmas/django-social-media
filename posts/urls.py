from django.urls import path
from .views import post_list_view, like_unlike_post

urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('liked/', like_unlike_post, name='like-post-view'),

]
