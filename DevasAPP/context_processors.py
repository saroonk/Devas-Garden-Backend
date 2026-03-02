from .views import get_or_create_cart 



def cart_count(request):
    cart = get_or_create_cart(request)

    count = cart.cartitem_set.count()


    return {
        'cart_count': count
    }
