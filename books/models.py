from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    bookid = models.CharField(max_length=20)  # google bookid
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    published = models.CharField(max_length=20)
    isbn = models.CharField(max_length=15)
    pages = models.CharField(max_length=5)
    language = models.CharField(max_length=2)
    description = models.TextField()
    inserted = models.DateTimeField('inserted', auto_now_add=True)
    edited = models.DateTimeField('last modified', auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.bookid, self.title)


class Search(models.Model):
    term = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    inserted = models.DateTimeField('inserted', auto_now_add=True)

    def __str__(self):
        return self.term
