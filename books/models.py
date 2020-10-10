from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

READING = 'r'
COMPLETED = 'c'
TO_READ = 't'
QUOTE = 'q'
NOTE = 'n'


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
    imagesize = models.CharField(max_length=2, default="1")
    inserted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    @property
    def title_and_authors(self):
        return f'{self.title} ({self.authors})'

    @property
    def url(self):
        return f'http://pbreadinglist.herokuapp.com/books/{self.bookid}'

    def __str__(self):
        return f'{self.id} {self.bookid} {self.title}'


class Search(models.Model):
    term = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    inserted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term


class UserBook(models.Model):
    READ_STATUSES = (
        (READING, 'I am reading this book'),
        (COMPLETED, 'I have completed this book'),
        (TO_READ, 'I want to read this book'),  # t of 'todo'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=READ_STATUSES,
    default=COMPLETED)
    completed = models.DateTimeField(default=timezone.now)
    inserted = models.DateTimeField(auto_now_add=True)  # != completed
    updated = models.DateTimeField(auto_now=True)

    @property
    def done_reading(self):
        return self.status == COMPLETED

    def __str__(self):
        return f'{self.user} {self.book} {self.status} {self.completed}'

    class Meta:
        ordering = ['-completed', '-id']


class BookNote(models.Model):
    NOTE_TYPES = (
        (QUOTE, 'Quote'),
        (NOTE, 'Note'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    userbook = models.ForeignKey(UserBook, on_delete=models.CASCADE, blank=True, null=True)
    type_note = models.CharField(max_length=1, choices=NOTE_TYPES, default=NOTE)
    description = models.TextField()
    public = models.BooleanField(default=False)
    inserted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    @property
    def quote(self):
        return self.type_note == QUOTE

    @property
    def type_note_label(self):
        for note, label in self.NOTE_TYPES:
            if note == self.type_note:
                return label.lower()
        return None

    def __str__(self):
        return f'{self.user} {self.userbook} {self.type_note} {self.description} {self.public}'


class Badge(models.Model):
    books = models.IntegerField()
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.books} -> {self.title}'
