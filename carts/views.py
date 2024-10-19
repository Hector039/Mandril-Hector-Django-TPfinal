from django.shortcuts import render, get_object_or_404
from users.models import CustomUser
from products.models import Product
from products.forms import ProductSearchForm
from .models import Cart
from django.contrib.auth.decorators import login_required

@login_required
def getUserCart(req, uid, msg='', err=''):
    try:
        userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
        cart = Cart.objects.filter(userId=uid)
        for prod in cart:
            prod.subtotal = prod.productId.price * prod.quantity

        total = 0
        for subTotal in cart:
            total = total + subTotal.subtotal

        return render(req, "cart-detail.html", {"avatar_url": userLogued, "cart": cart, "total": total, "message": msg})
    except Exception:
        return render(req, "cart-detail.html", {"avatar_url": userLogued, "cart": cart, "total": total, "error": err})
    
    

@login_required
def getCart(req, uid):
    return getUserCart(req, uid)

@login_required
def emptyCart(req, uid):
    try:
        cart = Cart.objects.filter(userId=uid).delete()
        if cart[0] != 0:
            return getUserCart(req, uid, msg='Cart is now empty.')
    except Exception as error:
        return getUserCart(req, uid, err=error)

@login_required
def deleteProductCart(req, uid, pid):
    try:
        user = CustomUser.objects.get(id=uid)
        product = Product.objects.get(id=pid)
        cart = Cart.objects.get(userId=user, productId=product).delete()
        if cart[0] != 0:
            return getUserCart(req, uid, msg=f'The product ID: {pid} was successfully removed.')
    except Exception as error:
        return getUserCart(req, uid, err=error)

@login_required
def buyCart(req, uid):
    return getUserCart(req, uid, msg='Coming soon.')

@login_required
def addToCart(req, uid, pid):
    searchForm = ProductSearchForm(req.GET)
    userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
    if req.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=uid)
            product = Product.objects.get(pk=pid)
            newProductToCart = Cart(id=None, userId=user, productId=product, quantity=req.POST["quantity"])
            newProductToCart.save()
            products = Product.objects.all()
            return render(req, "home.html", {"avatar_url": userLogued, "products": products, 'searchForm': searchForm})
        except Exception as error:
            products = Product.objects.all()
            return render(req, "home.html", {"avatar_url": userLogued, "products": products, "error": error, 'searchForm': searchForm})
        
    return getUserCart(req, uid)
