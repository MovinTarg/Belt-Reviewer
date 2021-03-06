# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(req):
    context = {
        'user_name': req.session['name'],
        'books': Book.objects.all(),
        'reviews': Review.objects.all().order_by('-created_at')[:3],
    }
    return render(req, 'books/index.html', context)

def add(req):
    context = {
        'user_id': req.session['user_id'],
        'authors': Author.objects.all()
    }
    return render(req, 'books/add.html', context)

def create(req):
    ret_vals = Author.objects.basic_validator(req.POST)
    errors = ret_vals[0]
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/books/add')
    errors = Book.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/books/add')
    errors = Review.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/books/add')
    
    req.session['author'] = ret_vals[1]
    if not Author.objects.filter(name = req.session['author']):
        Author.objects.create(name= req.session['author'])
    Book.objects.create(title=req.POST['title'], authors= Author.objects.get(name= req.session['author']))
    book = Book.objects.get(title=req.POST['title'], authors =  Author.objects.get(name= req.session['author']))
    book.books_review.create(review=req.POST['review'], rating = req.POST['rating'], reviewer = User.objects.get(id=req.session['user_id']))

    return redirect('/books/{}'.format(book.id))

def books(req, book_id):
    context = {
        'books': Book.objects.get(id = book_id),
        'reviews': Review.objects.filter(books = book_id),
        'user_id': req.session['user_id']
    }
    return render(req, 'books/books.html', context)

def review(req, book_id):
    errors = Review.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/books/{}'.format(book_id))
    Review.objects.create(review=req.POST['review'], rating = req.POST['rating'], books = Book.objects.get(id=book_id), reviewer = User.objects.get(id=req.session['user_id']))
    return redirect('/books/{}'.format(book_id))

def delete(req, book_id, review_id):
    Review.objects.get(id = review_id).delete()
    return redirect('/books/{}'.format(book_id))