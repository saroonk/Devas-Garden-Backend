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


def index(request):
    hero = HeroSection.objects.prefetch_related('images').first()

    offer = OfferBanner.objects.filter(is_active=True).first()

    testimonials = Testimonial.objects.filter(is_active=True)
    blogs =Blog.objects.select_related('category').all()[:3]

    return render(request, 'index.html',{'hero':hero,'offer':offer,'test':testimonials, 'blogs': blogs})



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
    return render(request, 'checkout.html')



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

def productdetails(request):
    return render(request, 'productdetails.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def returnpolicy(request):
    return render(request, 'returnpolicy.html')

def terms(request):
    return render(request, 'terms.html')

def trackorder(request):
    return render(request, 'trackorder.html')




@require_POST
def add_to_cart(request):
    print("Add to cart request received")
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

   
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = cart.cartitem_set.count()


    print(f"Product {product.name} added to cart. Total items in cart: {cart_count}")

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
        subtotal = product.price * quantity


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