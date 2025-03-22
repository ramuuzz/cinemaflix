from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('rentals/', views.user_rentals, name='user_rentals'),
    path('rentals/return/<int:transaction_id>/', views.return_movie, name='return_movie'),
]