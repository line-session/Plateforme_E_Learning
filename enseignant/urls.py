from django.urls import path

from plateforme import settings
from . import views

urlpatterns = [
    path('home', views.home, name='home_enseignant'),
    path('', views.home, name='home_enseignant'),
    path('sign-up', views.sign_up, name='sign_up_enseignant'),
    path('login', views.login_views, name='login_enseignant'),
    path('handle', views.logout_views, name='logout_enseignant'),
    path('cours', views.cours, name='cours_enseignant'),
    path('cours/add', views.add, name='add_cours_enseignant'),
    path('cours/delete/<int:id>', views.delete_course, name='delete_course'),
    path('cours/update/<int:id>', views.update_course, name='update_course'),
    path('cours/media/<int:id>', views.video_page, name='media_course'),
]