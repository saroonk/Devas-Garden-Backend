from django.shortcuts import render

from .models import *

from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.conf import settings
import threading

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


import json
import razorpay
from django.conf import settings

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def get_or_create_cart(request):
    """
    Get or create cart based on user or session.
    For authenticated users: use user field
    For guests: use session_id from Django session
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    return cart


def MailSender(full_name, mobile_number, subject, email, user_message):
    
    subject = f"New Contact Submission: {subject}"

    message = f"Name: {full_name}\n"
    message += f"Mobile Number: {mobile_number}\n"
    
    message += f"Email: {email}\n"
    message += f"Message: {user_message}"

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.EMAIL_HOST_USER]

    send_mail(subject, message, from_email, recipient_list)




def send_replacement_email(name, email, phone, orderdetails_id, reason, details):

    subject = f"New Replacement Request for Order #{orderdetails_id}"

    message = f"Name: {name}\n"
    message += f"Email: {email}\n"
    message += f"Phone: {phone}\n"
    message += f"Order ID: {orderdetails_id}\n"
    message += f"Reason: {reason}\n"
    message += f"Details: {details}"

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.DEFAULT_FROM_EMAIL]

    send_mail(subject, message, from_email, recipient_list)



def send_order_email(order):

    subject = f"Your Order Has Been Confirmed - {order.id}"

    html_content = render_to_string(
        "emails/order_confirmation.html",
        {
            "name": f"{order.first_name} {order.last_name}",
            "order_id": order.id,
            "items": order.items.all()
        }
    )

    email = EmailMultiAlternatives(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()



def send_owner_order_email(order):

    subject = f"New Order Received - {order.id}"

    html_content = render_to_string(
        "emails/new_order_notification.html",
        {
            "name": f"{order.first_name} {order.last_name}",
            "order_id": order.id,
            "email": order.email,
            "phone": order.phone,
            "items": order.items.all()
        }
    )

    email = EmailMultiAlternatives(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

def index(request):
    hero = HeroSection.objects.prefetch_related('images').first()

    offer = OfferBanner.objects.filter(is_active=True).first()

    testimonials = Testimonial.objects.filter(is_active=True)
    blogs =Blog.objects.select_related('category').all()[:3]

    top = Product.objects.filter(is_featured=True).select_related("category", "subcategory").prefetch_related("images")[:8]
    bottom = Product.objects.filter(is_featured=False).select_related("category", "subcategory").prefetch_related("images")[:8]

    return render(request, 'index.html',{'hero':hero,'offer':offer,'test':testimonials, 'blogs': blogs, 'topproducts': top, 'bottomproducts': bottom})



def login_view(request):

    if request.method == "POST":    
        username = request.POST.get("username")
        password = request.POST.get("password")

        # print(f"Username: {username}, Password: {password}") 


        user = authenticate(request, username=username , password=password)

        # print(f"Authenticated User: {user}")  

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("uName")  
        first_name = request.POST.get("fName")
        last_name = request.POST.get("lName")
        email = request.POST.get("signupEmail")
        phone = request.POST.get("signupPhone")
        password = request.POST.get("signupPassword")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect("register")

 
        
        try:
            user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

            user.first_name = first_name
            user.last_name = last_name
            user.save()

        
            Profile.objects.create(
                user=user,
                phone=phone
            )
            messages.success(request, "Registration successful! Please log in.")

        except Exception as e:
            messages.error(request, f"Registration failed")


        return redirect("login")  

    return render(request, "register.html")

    
def bloglisting(request):
    blogcategories = BlogCategory.objects.all()
    blogs = Blog.objects.select_related('category').order_by('-uploaded_date')

    paginator = Paginator(blogs, 15) 
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request, 'bloglisting.html', {'blogcategories': blogcategories, 'blogs': blogs})

def blogdetails(request, slug):
    blog = Blog.objects.get(slug=slug)
    related = Blog.objects.filter(category=blog.category).exclude(id=blog.id)[:3]
    return render(request, 'blogdetails.html', {'blog': blog, 'related': related})

def cart(request):
    cart = get_or_create_cart(request)
  
    cart_items = cart.cartitem_set.select_related('product').all()
    # cart_items = cart.cartitem_set.select_related('product').all()

    total = cart.total_amount

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == 'remove':
            cart_item.delete()
            messages.success(request, "Item removed from cart.")

        return redirect('cart')
    return render(request, 'cart.html', {'cart': cart_items,'total': total})









def checkout(request):

    cart = get_or_create_cart(request)

    cart_items = cart.cartitem_set.select_related('product')

    states = State.objects.all()

    # print("Checkout page loaded ----------------------------")

    for item in cart_items:

        if item.product.stock < item.quantity:

            messages.error(
                request,
                f"Sorry! Only {item.product.stock} units of '{item.product.title}' are available."
            )

            return redirect('cart')
        
        if item.quantity<=0:
            messages.error(
                request,
                f"Sorry! product quantity must be minimum 1 ."
            )
            return redirect('cart')



    context = {
        "cart": cart,
        "cart_items": cart_items
        ,"states": states
    }

    return render(request, 'checkout.html', context)



from decimal import Decimal

def calculate_shipping(request):

    state_id = request.GET.get("state_id")

    cart = get_or_create_cart(request)

    state = State.objects.get(id=state_id)

    data = cart.calculate_shipping(state)

    return JsonResponse({
        "shipping": float(data["shipping"]),
        "subtotal": float(data["subtotal"]),
        "total": float(data["total"])
    })




def contactus(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        mobile_number = request.POST.get("mobile_number")
        subject = request.POST.get("subject")
       
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save to DB
        ContactSubmission.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            subject=subject,
            email=email,
            message=message,
        )

        # Start background email thread
        thread = threading.Thread(
            target=MailSender,
            args=(full_name, mobile_number, subject, email, message),
        )
        thread.start()

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contactus")
    return render(request, 'contactus.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def productdetails(request, slug):
    product = (Product.objects.select_related("category", "subcategory")
                .prefetch_related("images")).get(slug=slug)

    
    in_wishlist = False

    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()
    else:
        if request.session.session_key:
            in_wishlist = Wishlist.objects.filter(
                session_id=request.session.session_key,
                product=product
            ).exists()

    featured_products = Product.objects.filter(is_featured=True).exclude(id=product.id)[:4]
    return render(request, 'productdetails.html', {'product': product, 'featured_products': featured_products,"in_wishlist": in_wishlist   })




from .filter import ProductFilter
def products(request, slug=None):



    products = (
        Product.objects
        .select_related("category", "subcategory")
        .prefetch_related("images")
        .order_by("-created_at")
    )

    selected_category = None
    selected_subcategory = None

    if slug:
        # Try Category first
        category = Category.objects.filter(slug=slug).first()

        if category:
            selected_category = category
            products = products.filter(category=category)
        else:
            # Try SubCategory
            subcategory = get_object_or_404(SubCategory, slug=slug)
            selected_subcategory = subcategory
            products = products.filter(subcategory=subcategory)

    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs

    paginator = Paginator(products,50)
    page_number = request.GET.get("page")
    page_obj =paginator.get_page(page_number)
    productscount = products.count()
    context = {
        "page_obj": page_obj,
        "product_filter": product_filter,
        "selected_category": selected_category,
        "selected_subcategory": selected_subcategory,
            "productscount": productscount
    }


    if request.htmx:
        return render(request, "partial/products.html", context)

    return render(request, "products.html", context)


def returnpolicy(request):
    return render(request, 'returnpolicy.html')

def terms(request):
    return render(request, 'terms.html')

def shippinganddeliveryPolicy(request):
    return render(request, 'shippinganddeliveryPolicy.html')

def trackorder(request):
    orders = None



    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        orderdetails_id = request.POST.get("order_id")
        reason = request.POST.get("reason")
        details = request.POST.get("details")

        proof = request.FILES.get("proof")

        order = Order.objects.filter(id=orderdetails_id).first()

        user = request.user if request.user.is_authenticated else None


    
        if not request.user.is_authenticated:

            try:
                order = Order.objects.get(id=orderdetails_id, email=email)
            except Order.DoesNotExist:
                messages.error(request, "No order found with the provided email and order ID.")
                return redirect("trackorder")


            

        ReplacementRequest.objects.create(
            User=user,
            order=order,
            name=name,
            email=email,
            phone=phone,
            orderdetails_id=orderdetails_id,
            reason=reason,
            details=details,
            proof=proof
        )

        thread = threading.Thread(
            target=send_replacement_email,
            args=(name, email, phone, orderdetails_id, reason, details)
        )
        thread.start()
        messages.success(request, "Your replacement request has been submitted successfully.")
        return redirect("trackorder")


    if request.method == "GET" and request.GET.get("trackmail"):
        email = request.GET.get("trackmail")
        orders = Order.objects.filter(email=email).order_by("-created_at")

    elif request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "trackorder.html", {"orders": orders , "order_count": orders.count() if orders else 0})




# @require_POST
# def add_to_cart(request):
#     print("Add to cart request received")
#     product_id = request.POST.get('product_id')
#     product = Product.objects.get(id=product_id)

   
#     cart = get_or_create_cart(request)

#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product
#     )

#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     cart_count = cart.cartitem_set.count()


#     print(f"Product {product.title} added to cart. Total items in cart: {cart_count}")

#     return JsonResponse({
#         'status': 'success',
#         'cart_count': cart_count
#     })




@require_POST
def add_to_cart(request):
    print("Add to cart request received")
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    quantity = int(request.POST.get('quantity', 1))  # default 1

    print(f"Requested quantity: {quantity} for product {product.title}")

    if quantity<1:
        return JsonResponse({
        'status': 'failed',
    })



   
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    cart_count = cart.cartitem_set.count()


    print(f"Product {product.title} added to cart. Total items in cart: {cart_count}")

    return JsonResponse({
        'status': 'success',
        'cart_count': cart_count
    })



@require_POST
def update_cart_quantity(request):
    print("Update cart quantity request received")
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))



    try:
        cart = get_or_create_cart(request)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()


        product = cart_item.product
        subtotal = product.new_price * quantity


        # subproduct = Product.objects.get(id=product_id)
        # subtotal = subproduct.price * quantity
        # print("______________",subtotal)
    except Exception:
        return messages.error("No cart appeared")

    # cart_count = cart.cartitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return JsonResponse({
        'status': 'success',
        'subtotal':float(subtotal),
        'total': float(cart.total_amount),
        # 'cart_count': cart_count
    })






def wishlist(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(
            wishlist__user=request.user
        )
    else:
        if not request.session.session_key:
            request.session.create()

        products = Product.objects.filter(
            wishlist__session_id=request.session.session_key
        )

    return render(request, 'wishlist.html', {'products': products})

def add_to_wishlist(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).first()
        print("User is authenticated. Checking wishlist for user.")
    else:
        if not request.session.session_key:
            request.session.create()

        wishlist_item = Wishlist.objects.filter(
            session_id=request.session.session_key,
            product=product
        ).first()
        print("User is not authenticated. Checking wishlist for session.")

    if wishlist_item:
        wishlist_item.delete()
        status = "removed"
        print(f"Product {product.title} removed from wishlist.")
    else:
        if request.user.is_authenticated:
            Wishlist.objects.create(
                user=request.user,
                product=product
            )
            print(f"Product {product.title} added to wishlist for user {request.user.username}.")
        else:
            Wishlist.objects.create(
                session_id=request.session.session_key,
                product=product
            )
        status = "added"
        print(f"Product {product.title} added to wishlist for session {request.session.session_key}.")  
    
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = Wishlist.objects.filter(
            session_id=request.session.session_key
        ).count()
    print(f"Received wishlist request for product ID: {product_id}")

    return JsonResponse({
        'success': True,
        'status': status,
        'wishlist_count': wishlist_count
    })


def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=query)

    paginator = Paginator(products, 50) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    productscount = products.count()
    search_query = query

    context = {
        'query': query,
        'page_obj': page_obj,
        'productscount': productscount,
        'search_query': search_query
    }
    return render(request, 'products.html', context)










from django.db import transaction


import traceback
@transaction.atomic
def place_order(request):

    cart = get_or_create_cart(request)
    cart_items = cart.cartitem_set.select_related("product")

    for item in cart_items:

        if item.product.stock < item.quantity:

            messages.error(
                request,
                f"Sorry! Only {item.product.stock} units of '{item.product.title}' are available."
            )

            return redirect('cart')

    if request.method == "POST":

        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        address = request.POST.get("address")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state_id = request.POST.get("state")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")
        email = request.POST.get("email")



        state = State.objects.get(id=state_id)

        data = cart.calculate_shipping(state)

        subtotal = data["subtotal"]
        shipping = data["shipping"]
        total = data["total"]

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email,
            first_name=first_name,
            last_name=last_name,
            address1=address,
            address2=address2,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            subtotal=subtotal,
            shipping_charge=shipping,
            total=total
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.new_price,
                total_price=item.product.new_price * item.quantity
            )


        print("==========================================order created with total:", order.total )


        print("===========================================Initiating Razorpay payment for order:", order.id, "with amount:", total)

        

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        print("Razorpay client initialized with key:", settings.RAZORPAY_KEY_ID)
        print("Creating Razorpay order with amount (in paise):", int(total * 100))
        print(client)
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        print("-----------------------------------------------")
        print("KEY:", settings.RAZORPAY_KEY_ID)
        print("SECRET:", settings.RAZORPAY_KEY_SECRET)

        try:
            payment = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": "1"
        })
            # razorpay_order = client.order.create({
            #     "amount": int(total * 100),  
            #     "currency": "INR",
            #     "payment_capture": 1
            #     })
        except Exception as e:
            print("RAZORPAY ERROR:")
            traceback.print_exc()

            messages.error(request, "There was an error initiating payment. Please try again.")
            return redirect('checkout')

        print("Razorpay order created:---------------------------------", payment)






        order.razorpay_order_id = payment["id"]
        order.save()

        context = {
            "order": order,
            "payment": payment,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        }

        return render(request,"payment.html",context)




# def payment_success(request):

#     data = json.loads(request.body)

#     razorpay_order_id = data["razorpay_order_id"]
#     razorpay_payment_id = data["razorpay_payment_id"]

#     order = Order.objects.get(razorpay_order_id=razorpay_order_id)

#     order.payment_status = "paid"
#     order.razorpay_payment_id = razorpay_payment_id
#     order.status = "processing"

#     order.save()



#     for item in order.items.all():

#         product = item.product
#         product.stock -= item.quantity
#         product.save()

  
#     cart = get_or_create_cart(request)
#     cart.cartitem_set.all().delete()

#     return JsonResponse({"status":"success"})





@transaction.atomic
def payment_success(request):



    data = json.loads(request.body)

    razorpay_order_id = data["razorpay_order_id"]
    razorpay_payment_id = data["razorpay_payment_id"]
    razorpay_signature = data["razorpay_signature"]

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )



    try:

        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })




    except:

        return JsonResponse({"status": "payment_failed"})


    order = Order.objects.get(razorpay_order_id=razorpay_order_id)
    if not order:
        return JsonResponse({"status": "order_not_found"})


    if order.payment_status == "paid":
        return JsonResponse({"status": "success"})

    order.payment_status = "paid"
    order.razorpay_payment_id = razorpay_payment_id
    order.razorpay_signature = razorpay_signature
    order.status = "processing"

    order.save()

    for item in order.items.all():

        product = item.product
        product.stock -= item.quantity
        product.save()

  
    cart = get_or_create_cart(request)
    cart.cartitem_set.all().delete()




    order_items = ""
    for item in order.items.all():
        order_items += f"- {item.product.title} (Qty: {item.quantity})\n"




    thread = threading.Thread(
        target=send_order_email,
        args=(order,)
    )
    thread.start()
    


    thread_owner = threading.Thread(
        target=send_owner_order_email,
        args=(order,)
    )
    thread_owner.start()

    return JsonResponse({"status":"success"})

def order_success(request):




    return render(request,"order_success.html")