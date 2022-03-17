from django.db import models
from datetime import date
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a movie genre.')
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=date.today)
    producer = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the movie')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this movie')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


## Guide for review found at https://www.youtube.com/watch?v=Y5vvGQyHtpM

class Review(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review', args=[str(self.id)])

class Request(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('review', args=[str(self.id)])

