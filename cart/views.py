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
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

    cart_quantity = cart.__len__()
    
    cart_total = cart.get_total()
    
    response = JsonResponse({'qty':cart_quantity,'total':cart_total})
    
    return response
    

import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity'))
            
            logger.debug(f"Product ID: {product_id}, Product Quantity: {product_quantity}")
            print("bộ đôi này là: ", product_id," và ",product_quantity)
            # Ensure product_quantity is positive
            if product_quantity <= 0:
                raise ValueError("Product quantity must be greater than zero.")
            
            cart.update(product=product_id, qty=product_quantity)
            
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid input: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    cart_quantity = cart.__len__()
    cart_total = cart.get_total()
    
    response = JsonResponse({'qty': cart_quantity,'total': cart_total})
    
    return response
