from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm, ChangePasswordForm
from .models import CustomUser
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from products.forms import ProductSearchForm
from django.contrib import messages
from products.models import Product
from chats.models import Message
import datetime
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

class signInView(View):
    loginForm = CustomUserLoginForm
    searchForm = ProductSearchForm
    templateName = "signin.html"

    def get(self, request):
        form = self.loginForm()
        return render(request, self.templateName, {"form": form})
    
    def post(self, request):
        form = self.loginForm(request.POST)
        if request.POST['email'] and request.POST['password']:
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
            
            if user is None:
                form = self.loginForm()
                messages.error(request, "User name o password incorrect")
                return render(request, self.templateName, {"form": form})
            
            login(request, user)
            searchForm = ProductSearchForm(request.GET)
            userLogued = get_object_or_404(CustomUser, pk=user.id)
            request.session["last_login"] = userLogued.last_login.strftime("%d/%m/%Y %H:%M:%S")
            request.session["avatar_path"] = userLogued.avatar.url
            userLogued.last_login = datetime.datetime.now()
            userLogued.save()
            products = Product.objects.all()
            msgsUnreaded = Message.objects.filter(Q(to_id=userLogued, seen=False)).count()

            if msgsUnreaded != 0:
                messages.warning(request, f"You have {msgsUnreaded} unread messages.")

            return render(request, 'home.html', {"avatar_url": request.session["avatar_path"], "last_login": request.session["last_login"], 'products': products, 'searchForm': searchForm})
        return render(request, self.templateName, {"form": form})

class signUpView(View):
    signUpForm = CustomUserCreationForm
    templateName = "signup.html"

    def get(self, request):
        form = self.signUpForm()
        return render(request, self.templateName, {"form": form})

    def post(self, request):
        if request.POST["password1"] == request.POST["password2"]:
            try:
                CustomUser.objects.create_user(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST["email"], password = request.POST["password1"], age = request.POST["age"])
                messages.success(request, "User registered successfully")
                return redirect('home')
            except IntegrityError:
                form = self.signUpForm()
                messages.error(request, "You must be over 18 years old to register")
                return render(request, self.templateName, {"form": form})
        form = self.signUpForm()
        messages.error(request, "Passwords do not match")
        return render(request, self.templateName, {"form": form})
            
class updateUserView(View):
    updateUserForm = CustomUserUpdateForm
    templateName = "account.html"

    @method_decorator(login_required)
    def get(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        form = self.updateUserForm(instance=user)
        return render(request, self.templateName, {"form": form, "last_login": request.session["last_login"], "date_joined": user.date_joined.strftime("%d/%m/%Y %H:%M:%S"), "avatar_url": request.session["avatar_path"]})
    
    @method_decorator(login_required)
    def post(self, request):
        try:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            if len(request.FILES) == 1:
                user.avatar = request.FILES["avatar"]
            form = self.updateUserForm(request.POST, instance=user)
            form.save()
            messages.success(request, "User updated successfully")
            return render(request, self.templateName, {"form": form, "last_login": request.session["last_login"], "date_joined": user.date_joined.strftime("%d/%m/%Y %H:%M:%S"), "avatar_url": request.session["avatar_path"]})
        except Exception as error:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            form = self.updateUserForm(request.POST, instance=user)
            messages.error(request, error)
            return render(request, self.templateName, {"form": form, "last_login": request.session["last_login"], "date_joined": user.date_joined.strftime("%d/%m/%Y %H:%M:%S"), "avatar_url": request.session["avatar_path"]})

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'change-password.html'
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        del self.request.session["last_login"]
        del self.request.session["avatar_path"]
        logout(self.request)
        messages.success(self.request, 'The password was changed correctly, please login again')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatar_url"] = self.request.session["avatar_path"]
        context["last_login"] = self.request.session["last_login"]
        return context

@login_required
def closeSession(req):
    del req.session["last_login"]
    del req.session["avatar_path"]
    logout(req)
    return redirect('home')
