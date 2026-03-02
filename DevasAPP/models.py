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





class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_available(self, quantity=1):
        return self.stock >= quantity





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


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
