from django.shortcuts import render, get_object_or_404
from .models import Product
from .forms import ProductForm, ProductSearchForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required

def getProducts(req):
    searchForm = ProductSearchForm(req.GET)
    data = searchForm.data.get('title') if searchForm.data.get('title') is not None else ''
    category = searchForm.data.get('category')
    price = searchForm.data.get('price')
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    if category != 'all' and category is not None:
                if price == 'descending':
                    productsFiltered = Product.objects.filter(category=category).filter(title__icontains=data).order_by('-price').values()
                elif price == 'ascending':
                    productsFiltered = Product.objects.filter(category=category).filter(title__icontains=data).order_by('price').values()
                else:
                    productsFiltered = Product.objects.filter(category=category).filter(title__icontains=data)
                return render(req, "home.html", {"avatar_url": userLogued, "products": productsFiltered, 'searchForm': searchForm})
    else:
                if price == 'descending':
                    productsFiltered = Product.objects.filter(title__icontains=data).order_by('-price').values()
                elif price == 'ascending':
                    productsFiltered = Product.objects.filter(title__icontains=data).order_by('price').values()
                else:
                    productsFiltered = Product.objects.filter(title__icontains=data)
                return render(req, "home.html", {"avatar_url": userLogued, "products": productsFiltered, 'searchForm': searchForm})

def getProduct(req, pid):
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    product = get_object_or_404(Product, pk=pid)
    return render(req, "product-detail.html", {"avatar_url": userLogued, "product": product})

@login_required
def createProduct(req):
    productform = ProductForm()
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    if req.method == 'POST':
        try:
            owner = CustomUser.objects.get(id=req.user.id)
            Product.objects.create(title = req.POST["title"], description = req.POST["description"], price = req.POST["price"], stock = req.POST["stock"], category = req.POST["category"], owner = owner) 
            return render(req, "product-create.html", {"avatar_url": userLogued, "form": productform, "message": 'Product created successfully'})
        except Exception as error:
            return render(req, "product-create.html", {"avatar_url": userLogued, "form": productform, "error": error})
    else:
        return render(req, "product-create.html", {"avatar_url": userLogued, "form": productform})

@login_required
def updateProduct(req, pid):
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    if req.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=pid)
            productform = ProductForm(req.POST, instance=product)
            productform.save()
            return render(req, "product-update.html", {"avatar_url": userLogued, "form": productform, "product": product})
        except Exception as error:
            return render(req, "product-update.html", {"avatar_url": userLogued, "form": productform, "product": product, "error": error})
            
    product = get_object_or_404(Product, pk=pid)    
    productform = ProductForm(instance=product)
    return render(req, "product-update.html", {"avatar_url": userLogued, "form": productform, "product": product})

@login_required
def deleteProduct(req, pid):
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    product = get_object_or_404(Product, pk=pid)
    try:
        product.delete()
        searchForm = ProductSearchForm(req.GET)
        products = Product.objects.all()
        return render(req, "home.html", {"avatar_url": userLogued, "products": products, 'searchForm': searchForm})
    except Exception as error:
        productform = ProductForm(instance=product)
        return render(req, "product-update.html", {"avatar_url": userLogued, "form": productform, "product": product, "error": error})

@login_required
def buyProduct(req, pid):
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    products = Product.objects.all()
    searchForm = ProductSearchForm(req.GET)
    return render(req, "home.html", {"avatar_url": userLogued, "products": products, 'searchForm': searchForm, "message": 'Coming soon'})
