from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm, ProductSearchForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def getProducts(req):
    searchForm = ProductSearchForm(req.GET)
    data = searchForm.data.get('title') if searchForm.data.get('title') is not None else ''
    category = searchForm.data.get('category')
    price = searchForm.data.get('price')
    userLogued = get_object_or_404(CustomUser, pk=req.user.id) if req.user.id else '#'
    userAvatar = userLogued.avatar.url if req.user.id else '#'
    userLastLogin = req.session["last_login"] if req.user.id else '#'
    if category != 'all' and category is not None:
                if price == 'descending':
                    productsFiltered = Product.objects.filter(category=category).filter(title__icontains=data).order_by('-price').values()
                elif price == 'ascending':
                    productsFiltered = Product.objects.filter(category=category).filter(title__icontains=data).order_by('price').values()
                else:
                    productsFiltered = Product.objects.filter(category=category).filter(title__icontains=data)
                return render(req, "home.html", {"avatar_url": userAvatar, "last_login": userLastLogin, "products": productsFiltered, 'searchForm': searchForm})
    else:
                if price == 'descending':
                    productsFiltered = Product.objects.filter(title__icontains=data).order_by('-price').values()
                elif price == 'ascending':
                    productsFiltered = Product.objects.filter(title__icontains=data).order_by('price').values()
                else:
                    productsFiltered = Product.objects.filter(title__icontains=data)
                return render(req, "home.html", {"avatar_url": userAvatar, "last_login": userLastLogin, "products": productsFiltered, 'searchForm': searchForm})

class getProductView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = "product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userLogued = CustomUser.objects.get(pk=self.request.user.id) if self.request.user.id else '#'
        userAvatar = userLogued.avatar.url if self.request.user.id else '#'
        userLastLogin = self.request.session["last_login"] if self.request.user.id else '#'
        context["avatar_url"] = userAvatar
        context["last_login"] = userLastLogin
        return context

class createProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product-create.html"
    success_url = reverse_lazy('product-create')

    def form_valid(self, form):
        user = CustomUser.objects.get(pk=self.request.user.id)
        form.instance.owner = user
        form.save()
        messages.success(self.request, 'The product was created correctly')
        return super().form_valid(form)
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userLogued = CustomUser.objects.get(pk=self.request.user.id)
        context["avatar_url"] = userLogued.avatar.url
        context["last_login"] = self.request.session["last_login"]
        return context

@login_required
def updateProduct(req, pid):
    if req.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=pid)
            productform = ProductForm(req.POST, instance=product)
            productform.save()
            messages.success(req, 'The product was updated correctly')
            return render(req, "product-update.html", {"avatar_url": req.session["avatar_path"], "last_login": req.session["last_login"], "form": productform, "product": product})
        except Exception as error:
            messages.error(req, error)
            return render(req, "product-update.html", {"avatar_url": req.session["avatar_path"], "last_login": req.session["last_login"], "form": productform, "product": product})
            
    product = get_object_or_404(Product, pk=pid)    
    productform = ProductForm(instance=product)
    return render(req, "product-update.html", {"avatar_url": req.session["avatar_path"], "last_login": req.session["last_login"], "form": productform, "product": product})

@login_required
def deleteProduct(req, pid):
    product = get_object_or_404(Product, pk=pid)
    try:
        product.delete()
        searchForm = ProductSearchForm(req.GET)
        products = Product.objects.all()
        messages.success(req, 'The product was deleted correctly')
        return render(req, "home.html", {"avatar_url": req.session["avatar_path"], "last_login": req.session["last_login"], "products": products, 'searchForm': searchForm})
    except Exception as error:
        productform = ProductForm(instance=product)
        messages.error(req, error)
        return render(req, "product-update.html", {"avatar_url": req.session["avatar_path"], "last_login": req.session["last_login"], "form": productform, "product": product})

@login_required
def buyProduct(req, pid):
    products = Product.objects.all()
    searchForm = ProductSearchForm(req.GET)
    messages.warning(req, "Comming soon...")
    return render(req, "home.html", {"avatar_url": req.session["avatar_path"], "last_login": req.session["last_login"], "products": products, 'searchForm': searchForm})
