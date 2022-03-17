from . import views
from django.urls import path, re_path
from django.urls import include

app_name = 'movie-review'

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:pk>', views.movie_detail, name='movie_detail'),
    re_path(r'^home/$', views.home, name='home'),
    path('movie_list', views.movie_list, name='movie_list'),
    path('genre_list', views.genre_list, name='genre_list'),
    path('contact', views.contact, name='contact'),
    path('review/create/', views.review_new, name='review_new'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]