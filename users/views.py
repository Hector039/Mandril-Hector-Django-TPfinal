from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from products.forms import ProductSearchForm
from django.contrib import messages

def signIn(req):
    if req.method == "POST":
        try:
            user = authenticate(req, email=req.POST['email'], password=req.POST['password'])
        except Exception as error:
            render(req, "signin.html", {"form": CustomUserLoginForm, "error": error})

        if user is None:
            return render(req, "signin.html", {"form": CustomUserLoginForm, "error": "User name o password incorrect"})
        else:
            login(req, user)
            searchForm = ProductSearchForm(req.GET)
            userLogued = get_object_or_404(CustomUser, pk=user.id)
            messages.success(req, f"Welcome {userLogued.first_name}!")
            return render(req, 'home.html', {"avatar_url": userLogued.avatar.url, 'searchForm': searchForm})

    return render(req, "signIn.html", {"form": CustomUserLoginForm})

def signUp(req):
    if req.method == "POST":
        if req.POST["password1"] == req.POST["password2"]:
            try:
                CustomUser.objects.create_user(first_name = req.POST["first_name"], 
                                               last_name = req.POST["last_name"], 
                                               email = req.POST["email"], 
                                               password = req.POST["password1"], 
                                               age = req.POST["age"])
                return redirect('home')
            except IntegrityError:
                return render(req, "signup.html", {"form": CustomUserCreationForm, "error": "You must be over 18 years old to register"})
        else:
            return render(req,"signup.html", {"form": CustomUserCreationForm, "error": "Passwords must be equals"})
    return render(req, "signUp.html", {"form": CustomUserCreationForm})

@login_required
def closeSession(req):
    logout(req)
    return redirect('home')

@login_required
def updateUser(req):
    if req.method == 'POST':        
        try:
            user = get_object_or_404(CustomUser, pk=req.user.id)
            if len(req.FILES) == 1:
                user.avatar = req.FILES["avatar"]
            userUpdateform = CustomUserUpdateForm(req.POST, instance=user)
            userUpdateform.save()
            messages.success(req, "User updated successfully")
            return render(req, "account.html", {"form": userUpdateform, "avatar_url": user.avatar.url})
        except Exception as error:
            return render(req, "account.html", {"form": userUpdateform, "error": error, "avatar_url": user.avatar.url})
            
        
    user = get_object_or_404(CustomUser, pk=req.user.id)
    userUpdateform = CustomUserUpdateForm(instance=user)
    return render(req, "account.html", {"form": userUpdateform, "avatar_url": user.avatar.url})

