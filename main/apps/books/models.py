# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import *

# Create your models here.
class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        new_author = False
        errors = {}
        author = ''
        if len(postData['author2']) < 1:
            if not Book.objects.filter(authors=postData['author1']):
                errors['no_author'] = "Please select or add an author"
            if Book.objects.get(authors=postData['author1']):
                author=postData['author1']
        if len(postData['author2']) > 1:
            author=postData['author2']
        authors = Author.objects.all()
        print authors
        if not authors:
            new_author = True
        else:
            for saved_author in authors:
                print 'saved: ', saved_author
                print 'saved name: ', saved_author.name
                if saved_author.name != author:
                    new_author = True
        return errors, author, new_author
class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        books = Book.objects.all()
        for book in books:
            if book.title == postData['title']:
                errors['duplicate_book'] = "Book already in database"
        if len(postData['title']) < 1:
            errors["empty_title"] = "Title cannot be empty!"
        return errors
class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        reviews = Review.objects.all()
        if len(postData['review']) < 15:
            errors["short_name"] = "Review must be at least 15 characters long!"
        return errors

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = AuthorManager()
class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = BookManager()
class Review(models.Model):
    reviewer = models.ForeignKey(User)
    books = models.ForeignKey(Book, related_name='books_review')
    review = models.CharField(max_length=255)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ReviewManager()