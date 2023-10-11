from django.urls import path
from .views import post_list_view, like_unlike_post, PostDeleteView, PostUpdateView

urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='delete-view'),
    path('<pk>/update/', PostUpdateView.as_view(), name='update-view'),
]
