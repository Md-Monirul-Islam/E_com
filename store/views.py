from django.shortcuts import redirect, render,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from .models import Product
from django.contrib import messages

# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.all().filter(category=categories,is_available=True)
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_prodects = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_prodects = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products':paged_prodects,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        try:
            in_cart = CartItem.objects.get(cart__cart_id=_cart_id(request), product=single_product)
        except ObjectDoesNotExist:
            in_cart = False
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'is_out_of_stock': single_product.stock <= 0,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)
