from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from products.forms import ProductSearchForm
from django.contrib import messages
from products.models import Product
from chats.models import Message

def signIn(req):
    if req.method == "POST":
        try:
            user = authenticate(req, email=req.POST['email'], password=req.POST['password'])
        except Exception as error:
            messages.error(req, error)
            render(req, "signin.html", {"form": CustomUserLoginForm})

        if user is None:
            messages.error(req, "User name o password incorrect")
            return render(req, "signin.html", {"form": CustomUserLoginForm})
        else:
            login(req, user)
            searchForm = ProductSearchForm(req.GET)
            userLogued = get_object_or_404(CustomUser, pk=user.id)
            products = Product.objects.all()

            msgsUnreaded = Message.objects.filter(Q(to_id=userLogued, seen=False)).count()
            if msgsUnreaded != 0:
                messages.warning(req, f"You have {msgsUnreaded} unread messages.")

            return render(req, 'home.html', {"avatar_url": userLogued.avatar.url, 'products': products, 'searchForm': searchForm})

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
                messages.success(req, "User registered successfully")
                return redirect('home')
            except IntegrityError:
                messages.error(req, "You must be over 18 years old to register")
                return render(req, "signup.html", {"form": CustomUserCreationForm})
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
            messages.error(req, error)
            return render(req, "account.html", {"form": userUpdateform, "avatar_url": user.avatar.url})
            
        
    user = get_object_or_404(CustomUser, pk=req.user.id)
    userUpdateform = CustomUserUpdateForm(instance=user)
    return render(req, "account.html", {"form": userUpdateform, "avatar_url": user.avatar.url})

