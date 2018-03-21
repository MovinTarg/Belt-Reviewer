# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(req):
    return render(req, 'users/index.html')

def create(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/')
    User.objects.create(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()))
    return redirect('/')

def login(req):
    loggedUser = User.objects.get(email = req.POST['email'])
    if bcrypt.checkpw(req.POST['password'].encode(), loggedUser.password.encode()) == True:
        req.session['name'] = loggedUser.first_name
        req.session['id'] = loggedUser.id
        return redirect('/books')
    return redirect('/')

def users(req, user_id):
    context = {
        'user': User.objects.get(id = user_id)
    }
    return render(req, 'users/users.html', context)

def logout(req):
    return redirect('/')