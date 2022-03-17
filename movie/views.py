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
    return render(request, 'website/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    sumstars = \
        Review.objects.filter(movie=pk).aggregate(Sum('stars'))
    countstars = \
        Review.objects.filter(movie=pk).aggregate(Count('stars'))
    return render(request, 'website/movie_detail.html',
                  {'movie': movie, 'sumstars': sumstars, 'countstars': countstars})


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
