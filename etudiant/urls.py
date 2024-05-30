from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home_etudiant'),
    path('', views.home, name='home_etudiant'),
    path('sign-up', views.sign_up, name='sign_up_etudiant'),
    path('login', views.login_views, name='login_etudiant'),
    path('handle', views.logout_views, name='logout_etudiant'),
    path('cours', views.cours, name='cours_etudiant'),
    path('cours/search', views.search, name='search_s'),
    path('cours/media/<int:id>', views.video_page, name='media_course_s'),
    path('devoir/', views.display_devoir_s, name='devoir_s'),
    path('devoir/download/<int:id>', views.download_devoir_s, name='download_s'),

]