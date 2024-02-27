from django.contrib import admin
from .models import Movie, Artist, Gender

admin.site.register(Movie)
admin.site.register(Artist)
admin.site.register(Gender)
