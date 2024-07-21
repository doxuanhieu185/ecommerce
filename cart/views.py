from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Products
from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Products, id=product_id)

        cart.add(product=product, product_qty=product_quantity)

        cart_quantity = len(cart)
        response = JsonResponse({'qty': cart_quantity})

        return response

    return JsonResponse({'error': 'Invalid request'}, status=400)





def cart_delete(request):
    pass

def cart_update(request):
    pass
