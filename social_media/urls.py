from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import home_view
from social_media import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home-view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
