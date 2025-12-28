from django.contrib import admin
from pages.views import signup, profile
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Обработчики ошибок — обязательно на верхнем уровне!
handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', signup, name='registration'),
    path('profile/<str:username>/', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)