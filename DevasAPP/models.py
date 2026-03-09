from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator


from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from django.contrib.auth.models import User

from decimal import Decimal
from django.core.validators import MinValueValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class HeroSection(models.Model):
    subtitle = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    button_text = models.CharField(max_length=100)
    # button_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class HeroImage(models.Model):
    hero = models.ForeignKey(
        HeroSection,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="hero_images/")
    def __str__(self):
        return f"Image for {self.hero.title}"






class OfferBanner(models.Model):
    mobile_image = models.ImageField(upload_to="offers/")
    desktop_image = models.ImageField(upload_to="offers/")
    popup_offer_image = models.ImageField(upload_to="offers/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Offer Banner"









class BlogCategory(models.Model):



    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
  
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.CASCADE,
        related_name="blogs"
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    author = models.CharField(max_length=100)

    uploaded_date = models.DateTimeField(auto_now_add=True)

    read_time = models.PositiveIntegerField(
        help_text="Enter approximate read time in minutes (Example: 8 for 8-minute read)"
    )

    main_image = models.ImageField(upload_to="blogs/")

    content = RichTextField()

    class Meta:
        ordering = ['-uploaded_date']

    def save(self, *args, **kwargs):
   
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title





class Testimonial(models.Model):
    content = models.TextField()
    profile_image = models.ImageField(upload_to="testimonials/",blank=True, null=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Rating from 1 to 5"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"






class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)

    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"





# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
#     stock = models.PositiveIntegerField()
#     image = models.ImageField(upload_to='products/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#     def is_available(self, quantity=1):
#         return self.stock >= quantity



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
       
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    class Meta:
        unique_together = ('category', 'name')

    def save(self, *args, **kwargs):
     
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True)
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(default=False)  # For homepage featured products
    stock = models.PositiveIntegerField(default=0)
    # Basic Info
    title = models.CharField(max_length=255,blank=True)
    short_description = models.TextField(blank=True)

    # Pricing
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Main Image
    main_image = models.ImageField(upload_to="products/main/")

 
    key_features = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    how_to_use = models.TextField(blank=True)


    zones = models.ManyToManyField('Zone', through='ProductDeliveryCharge')

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure only one cart per user or session
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_cart', condition=models.Q(user__isnull=False)),
            models.UniqueConstraint(fields=['session_id'], name='unique_session_cart', condition=models.Q(session_id__isnull=False)),
        ]

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart for session {self.session_id}"

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.cartitem_set.all())


    def calculate_shipping(self, state):

        zone = state.zone

        shipping_total = Decimal("0.00")
        subtotal = Decimal("0.00")
        total_quantity = 0

        cart_items = self.cartitem_set.select_related("product")

        for item in cart_items:

            subtotal += item.product.new_price * item.quantity
            total_quantity += item.quantity

            charge = ProductDeliveryCharge.objects.filter(
                product=item.product,
                zone=zone
            ).first()

            if charge:
                shipping_total += charge.charge * item.quantity

        if total_quantity >= 50:
            shipping_total = Decimal("0.00")

        elif total_quantity >= 35:
            shipping_total -= shipping_total * Decimal("0.50")

        elif total_quantity >= 25:
            shipping_total -= shipping_total * Decimal("0.40")

        elif total_quantity >= 15:
            shipping_total -= shipping_total * Decimal("0.35")

        elif total_quantity >= 10:
            shipping_total -= shipping_total * Decimal("0.25")

        elif total_quantity >= 5:
            shipping_total -= shipping_total * Decimal("0.15")

        total = subtotal + shipping_total

        return {
            "subtotal": subtotal,
            "shipping": shipping_total,
            "total": total
        }


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('cart', 'product')



    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def subtotal(self):
        return self.product.new_price * self.quantity

















class Zone(models.Model):
    name = models.CharField(max_length=50)  # Zone A, Zone B
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


# -------------------------
# STATE
# Each state belongs to a Zone
# -------------------------
class State(models.Model):
    name = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="states")

    def __str__(self):
        return f"{self.name} ({self.zone.name})"










class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/sub/")

    def __str__(self):
        return f"Image for {self.product.title}"



# -------------------------
# PRODUCT DELIVERY CHARGE
# (Each product can have different delivery charge per zone)
# -------------------------
class ProductDeliveryCharge(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    charge = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('product', 'zone')

    def __str__(self):
        return f"{self.product.title} - {self.zone.name} - ₹{self.charge}"






class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}"













class Order(models.Model):

    STATUS_CHOICES = (
        ("pending","Pending"),
        ("processing","Processing"),
        ("on_the_way","On The Way"),
        ("delivered","Delivered"),
    )

    PAYMENT_STATUS = (
        ("pending","Pending"),
        ("paid","Paid"),
        ("failed","Failed"),
    )

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255,blank=True)

    city = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,null=True)

    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10,decimal_places=2)
    total = models.DecimalField(max_digits=10,decimal_places=2)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")


    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default="pending")

    razorpay_order_id = models.CharField(max_length=200,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=200,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product} x {self.quantity}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity













class ReplacementRequest(models.Model):

    REASON_CHOICES = [
        ("damaged_during_transit", "Damaged during transit"),
        ("incorrect_plant_received", "Incorrect plant received"),
        ("severe_wilting_health_issues", "Severe wilting / Health issues"),
        ("other", "Other"),
    ]

    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    orderdetails_id = models.CharField(max_length=50)

    reason = models.CharField(
        max_length=100,
        choices=REASON_CHOICES
    )

    details = models.TextField(blank=True, null=True)

    proof = models.FileField(
        upload_to="replacement_proofs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.name}"