from django.contrib import admin
from .models import Movie, Genre, Review, Request, Profile

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Request)
admin.site.register(Profile)
