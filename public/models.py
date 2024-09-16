from django.db import models

class ShoeyAwards(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='shoey_awards')

    def __str__(self):
        return self.name

class BOTY(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='boty')

    def __str__(self):
        return self.title
