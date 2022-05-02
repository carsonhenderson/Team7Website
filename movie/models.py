from django.db import models
from datetime import date
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.utils import timezone
from profanity.validators import validate_is_profane

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a movie genre.')
    def __str__(self):
        return self.name

## Favorites model tutorial found below, it has been adapted/refactored and changed
## https://www.youtube.com/watch?v=H4QPHLmsZMU

class Movie(models.Model):
    title = models.CharField(max_length=200, validators=[validate_is_profane])
    date = models.DateField(default=date.today)
    producer = models.CharField(max_length=200, validators=[validate_is_profane])
    director = models.CharField(max_length=200, validators=[validate_is_profane])
    summary = models.TextField(max_length=1000, validators=[validate_is_profane], help_text='Enter a brief description of the movie')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this movie')
    favorites = models.ManyToManyField(User, related_name='favorite', default=None, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


## Guide for review found at https://www.youtube.com/watch?v=Y5vvGQyHtpM

class Review(models.Model):
    title = models.CharField(max_length=200, validators=[validate_is_profane])
    content = models.TextField(blank=True, null=True, validators=[validate_is_profane])
    stars = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
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
    subject = models.CharField(max_length=200, validators=[validate_is_profane])
    content = models.TextField(blank=True, null=True, validators=[validate_is_profane])
    user = User
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('review', args=[str(self.id)])


## https://www.youtube.com/watch?v=Alua227cOmY for profile tutorial
## https://www.youtube.com/watch?v=rJ3Gcv2i0as as well

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True)
    bio = models.TextField(max_length=500, validators=[validate_is_profane], null=True, blank=True)
    image = models.ImageField(upload_to="movie/static/images/profile", default="movie/static/images/profile/default.png", null=True)
    websiteurl = models.TextField(validators=[URLValidator()], max_length=100, null=True, blank=True)
    twitterurl = models.TextField(validators=[URLValidator()], max_length=100, null=True, blank=True)
    instagramurl = models.TextField(validators=[URLValidator()], max_length=100, null=True, blank=True)
    facebookurl = models.TextField(validators=[URLValidator()], max_length=100, null=True, blank=True)
    private = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

