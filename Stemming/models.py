from django.db import models

class Instagram_comment(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Stemming(models.Model):
    tokens = models.CharField(max_length=50)
    stem = models.CharField(max_length=50)
    frek = models.CharField(max_length=50, default='SOME STRING')

    def __str__(self):
        return f'{self.tokens}'