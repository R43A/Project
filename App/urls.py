from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.staticfiles.views import serve
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/', login, name='login'),
    path('signup/',signup,name='signup'),
    path('profile/',profile,name="profile"),
    path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('logout/', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path('favicon.ico', serve, {'path': 'favicon.ico'}),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path("delete_banner_image/", delete_banner_image, name="delete_banner_image"),
    path("delete_profile_picture/", delete_profile_picture, name="delete_profile_picture"),
    path("confirm_email/<str:uidb64>/<str:token>/<str:new_email>/", confirm_email,name="confirm_email",),
    path('check_username_availability/', check_username_availability, name='check_username_availability'),
    path('profile/', profile, name='profile'),
    path('live/', live, name="live")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)