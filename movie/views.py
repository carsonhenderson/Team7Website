from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from _decimal import Decimal
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

now = timezone.now()


def home(request):
    return render(request, 'website/home.html',
                  {'movie': home})


def contact(request):
    return render(request, 'website/contact.html',
                  {'movie': home})


def genre_list(request):
    genres = Genre.objects.filter()
    return render(request, 'website/genre_list.html',
                  {'genres': genres})


def movie_list(request):
    movies = Movie.objects.filter()
    sumratings = []
    countratings = []
    for movie in movies:
            pk = movie.pk
            sumstars = \
               Review.objects.filter(movie=pk).aggregate(Sum('stars'))

            countstars = \
                Review.objects.filter(movie=pk).aggregate(Count('stars'))
            sumratings.append(sumstars)
            countratings.append(countstars)
    return render(request, 'website/movie_list.html', {'movies': movies, "sumstars": sumratings, "countstars": countratings})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    favorite = bool
    if movie.favorites.filter(id=request.user.id).exists():
        favorite = True
    sumstars = \
        Review.objects.filter(movie=pk).aggregate(Sum('stars'))
    countstars = \
        Review.objects.filter(movie=pk).aggregate(Count('stars'))
    return render(request, 'website/movie_detail.html',
                  {'movie': movie, 'sumstars': sumstars, 'countstars': countstars, 'favorite': favorite})

def genre_detail(request, pk):
    genres = Genre.objects.filter()
    genre = get_object_or_404(Genre, pk=pk)
    movie = get_object_or_404(Movie, pk=pk)
    movies = Movie.objects.filter()
    sumratings = []
    countratings = []
    for movie in movies:
            pk = movie.pk
            sumstars = \
               Review.objects.filter(movie=pk).aggregate(Sum('stars'))

            countstars = \
                Review.objects.filter(movie=pk).aggregate(Count('stars'))
            sumratings.append(sumstars)
            countratings.append(countstars)
    return render(request, 'website/genre_detail.html', {'movies': movies, "sumstars": sumratings, "countstars": countratings,
                                                         'genres': genres, 'genre': genre, 'movie': movie})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'website/profile_detail.html', {'profile': profile})


## Guide to restrict found at https://stackoverflow.com/questions/62023710/django-how-to-restrict-a-user-to-put-review-only-once

@login_required
def review_new(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            review.created_date = timezone.now()
            review.save()
            reviews = Review.objects.filter(created_date__lte=timezone.now())
            return redirect('movie-review:movie_detail', pk=review.movie_id)
    else:
        form = ReviewForm()
    return render(request, 'website/review_new.html', {'form': form})



@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            review.updated_date = timezone.now()
            review.save()
            reviews = Review.objects.filter(created_date__lte=timezone.now())
            return redirect('movie-review:movie_detail', pk=review.movie_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'website/review_edit.html', {'form': form})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('movie-review:movie_detail', pk=review.movie_id)

@login_required
def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            requestform = form.save(commit=False)
            requestform.user = request.user
            requestform.save()
            requestform.created_date = timezone.now()
            requestform.save()
            requestforms = Review.objects.filter(created_date__lte=timezone.now())
            messages.info(request, 'Your password has been changed successfully!')
            return redirect('movie-review:home')
    else:
        form = ContactForm()
    return render(request, 'website/contact_new.html', {'form': form})

@login_required
def fav_add(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    user = request.user
    if movie.favorites.filter(id=user.id).exists():
        movie.favorites.remove(request.user)
    else:
        movie.favorites.add(user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def fav_list(request):
    favorite = Movie.objects.filter(favorites=request.user)
    return render(request, 'website/favorites_list.html', {'favorite': favorite})

@login_required
def private_add(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile.private == True:
        profile.private = False
        profile.save()
    else:
        profile.private = True
        profile.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def profile_new(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('movie-review:profile_detail', pk=request.user.profile.pk)
    else:
        form = ProfileForm()
    return render(request, 'website/profile_new.html', {'form': form})

