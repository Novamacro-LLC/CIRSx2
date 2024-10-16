from django.db import models

class ShoeyAwards(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField(null=False, default=0)
    image = models.CharField(max_length=100, null=False, default='Shoey Award')

    def __str__(self):
        return self.name

class BOTY(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(null=True)
    year = models.IntegerField(null=False, default=0)
    image = models.CharField(max_length=100, null=False, default='Book of the Year')

    def __str__(self):
        return self.title
