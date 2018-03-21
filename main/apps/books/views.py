# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
def index(req):
    context = {
        'name': req.session['name'],
        'id': req.session['id']
    }
    return render(req, 'books/index.html', context)

def add(req):
    return render(req, 'books/add.html')

def create(req):
    errors = Author.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/books/add')
    errors = Review.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/books/add')
    Book.objects.create(title=req.POST['title'])
    temp_book = Book.objects.get().last()
    Author.objects.create(name=req.POST['name'], books=temp_book.id)
    Review.objects.create(review=req.POST['review'], rating=req.POST['rating'], books=temp_book.id, users='id')
    context = {
        'title': temp_book.title,
        'author': temp_book.author
    }
    return render(req, 'books/books.html', context)

def books(req):
    return redirect('/books')