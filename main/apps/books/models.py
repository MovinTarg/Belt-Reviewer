# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .models import *

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        authors = Author.objects.all()
        if len(postData['name']) < 1:
            errors["short_name"] = "Name cannot be empty!"
        return errors

class Author(models.Model):
    books = models.ManyToManyField(Book, related_name = "authors")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = AuthorManager()

class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        reviews = Review.objects.all()
        if len(postData['review']) < 15:
            errors["short_name"] = "Review must be at least 15 characters long!"
        return errors

class Review(models.Model):
    users = models.ForeignKey('users.User', related_name = "reviews")
    books = models.ForeignKey(Book, related_name = "reviews")
    review = models.CharField(max_length=255)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = ReviewManager()