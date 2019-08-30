from django.db import models

# Create your models here.
class News(models.Model):
    Media   = models.TextField()
    Date    = models.DateTimeField()
    Title   = models.TextField()
    Link = models.TextField()