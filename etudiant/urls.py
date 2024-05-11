from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home_etudiant'),
    path('', views.home, name='home_etudiant'),
    path('sign-up', views.sign_up, name='sign_up_etudiant'),
    path('login', views.login_views, name='login_etudiant'),
    path('handle', views.logout_views, name='logout_etudiant'),
]