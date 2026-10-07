from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500) # Link to a movie poster
    rating = models.FloatField(default=0.0)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title