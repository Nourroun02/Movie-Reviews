from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from moviereviews import views
from django.conf import settings
from django.conf.urls.static import static  # <-- Add this import

urlpatterns = [
    




     path('movies/search/', views.movie_search, name='movie_search'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/<int:movie_id>/review/', views.review_create, name='add_review'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add this block to serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)