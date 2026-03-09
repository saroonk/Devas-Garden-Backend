from django.contrib import admin

try:
    from unfold.admin import ModelAdmin as BaseAdmin
except Exception:
    from django.contrib.admin import ModelAdmin as BaseAdmin

from .models import *

from django.http import HttpResponse
from reportlab.pdfgen import canvas


class HeroImageInline(admin.TabularInline):
    model = HeroImage
    extra = 1


@admin.register(HeroSection)
class HeroSectionAdmin(BaseAdmin):
    list_display = ("title", "subtitle", "is_active", "created_at")
    list_filter = ("is_active",)
    inlines = [HeroImageInline]


    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(OfferBanner)
class OfferBannerAdmin(BaseAdmin):
    list_display = ("id", "is_active", "created_at")
    list_filter = ("is_active",)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)




@admin.register(Testimonial)
class TestimonialAdmin(BaseAdmin):
    list_display = ("name", "role", "rating", "is_active", "created_at")
    list_filter = ("rating", "is_active")
    search_fields = ("name", "role")








@admin.register(BlogCategory)
class BlogCategoryAdmin(BaseAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
 

@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    list_display = ('title', 'category', 'author', 'uploaded_date', 'read_time')
    list_filter = ('category', 'uploaded_date')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(ContactSubmission)
class ContactSubmissionAdmin(BaseAdmin):
    list_display = ("full_name", "email", "mobile_number", "subject")
    
    search_fields = ("full_name", "email", "subject")







@admin.register(Cart)
class CartAdmin(BaseAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username",)

@admin.register(CartItem)
class CartItemAdmin(BaseAdmin):
    list_display = ("product", "quantity", )
    search_fields = ("product__name",)




@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(BaseAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}







@admin.register(Zone)
class ZoneAdmin(BaseAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(State)
class StateAdmin(BaseAdmin):
    list_display = ("name", "zone")
    search_fields = ("name", "zone")



@admin.register(ProductDeliveryCharge)
class ProductDeliveryChargeAdmin(BaseAdmin):
    list_display = ("product", "zone", "charge")
    list_filter = ("zone",)
    search_fields = ("product__name", "zone__name")


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductDeliveryInline(admin.StackedInline):
    model = ProductDeliveryCharge
    extra= 0


class ProductAdmin(BaseAdmin):
    list_display = ("title", "category", "new_price","stock")
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductDeliveryInline]


admin.site.register(Product, ProductAdmin)



@admin.register(Wishlist)
class WishlistAdmin(BaseAdmin):
    list_display = ("user","product","added_at") 
    





 


 
def download_shipping_label(modeladmin, request, queryset):

    order = queryset.first()

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="shipping_label_{order.id}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica", 14)
    p.drawString(200, 800, "Shipping Label")

    p.setFont("Helvetica", 12)

    p.drawString(100, 760, f"Order ID: {order.id}")
    p.drawString(100, 730, f"Name: {order.first_name} {order.last_name}")
    p.drawString(100, 710, f"Phone: {order.phone}")

    p.drawString(100, 680, "Address:")
    p.drawString(120, 660, order.address1)

    if order.address2:
        p.drawString(120, 640, order.address2)

    p.drawString(120, 620, f"{order.city}")
    p.drawString(120, 600, f"Pincode: {order.pincode}")

    p.showPage()
    p.save()

    return response

download_shipping_label.short_description = "Download Shipping Label"




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "total_price")
    can_delete = False




@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ("id", "user", "email", "first_name", "last_name", "total", "created_at","status","payment_status")
    search_fields = ("user__username", "email", "first_name", "last_name")
    inlines = [OrderItemInline]
    list_filter = ("status", "payment_status", "created_at")
    actions = [download_shipping_label]

@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):    
    list_display = ("order", "product", "quantity", "price","total_price")
    search_fields = ("order__id", "product__name")











@admin.register(ReplacementRequest)
class ReplacementRequestAdmin(BaseAdmin):
    list_display = ("name", "email", "reason","order", "created_at")
    search_fields = ("email", "name")