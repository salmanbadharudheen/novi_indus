from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, Cartitem
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
from  .models import Cart


def demo(request):
    return HttpResponse("this is the begining")

def allprodcat(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        products_list=Product.objects.all().filter(category=c_page,available=True)
    else:
        products_list=Product.objects.all().filter(available=True)
    paginator=Paginator(products_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)
    return render(request,"category.html",{'category':c_page,'products':products})

def proDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})



#----------------------------------cartspec___________________________#


def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=cart_id(request)

        )
        cart.save(),
    try:
            cart_item=Cartitem.objects.get(product=product,cart=cart)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
            cart_item.save()
    except Cartitem.DoesNotExist:
            cart_item=Cartitem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            cart_item.save()
    return redirect( 'cartapp:cart_detail' )

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_items=Cartitem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartapp:cart_detail')

def cart_delete(request,product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cartitem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cartapp:cart_detail')

# ________________________________to update/delete/cart_____________


def add_product(request):
    if request.method == 'POST':

        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']

        product = Product.objects.create(
            name=name,
            description=description,
            price=price

        )

        product.save()

        return redirect('cartapp:allprodcat')

    return render(request, 'add_product.html')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        product.name = request.POST['name']
        product.description = request.POST ['description']
        product.price = request.POST['price']

        product.save()

        return redirect('cartapp:allprodcat')

    return render(request, 'edit_product.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        product.delete()

        return redirect('cartapp:allprodcat')

    return render(request, 'delete_product.html', {'product': product})