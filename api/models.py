from django.db import models

# Create your models here.

class movieInputModel(models.Model):
    movie = models.CharField(max_length=150)
    
    def __str__(self):
        return self.movie
    