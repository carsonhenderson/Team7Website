from . import views
from django.urls import path, re_path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, SearchResultsView

app_name = 'movie-review'

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:pk>', views.movie_detail, name='movie_detail'),
    path('genre/<int:pk>', views.genre_detail, name='genre_detail'),
    re_path(r'^home/$', views.home, name='home'),
    path('movie_list', views.movie_list, name='movie_list'),
    path('favorites_id/<int:pk>', views.fav_add, name='favorite'),
    path('favorites_list', views.fav_list, name='favorites_list'),
    path('genre_list', views.genre_list, name='genre_list'),
    path('contact', views.contact, name='contact'),
    path('contact/create/', views.contact_new, name='contact_new'),
    path('review/<int:pk>/create/', views.review_new, name='review_new'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('profile/<int:pk>/view', views.profile_detail, name="profile_detail"),
    path('profile/<int:pk>/edit', views.profile_edit, name="profile_edit"),
    path('profile/<int:pk>/delete', views.profile_delete, name="profile_delete"),
    path('profile/<int:pk>/private', views.private_add, name='private'),
    path('profile/create/', views.profile_new, name='profile_new'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

