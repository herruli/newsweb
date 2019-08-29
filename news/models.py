from django.db import models

# Create your models here.
class News(models.Model):
    Date    = models.DateTimeField()
    Title   = models.TextField()
    Link    = models.TextField()
    Media   = models.TextField()