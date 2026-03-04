from django.contrib import admin

try:
    from unfold.admin import ModelAdmin as BaseAdmin
except Exception:
    from django.contrib.admin import ModelAdmin as BaseAdmin

from .models import *
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
    extra = 4


class ProductAdmin(BaseAdmin):
    list_display = ("title", "category", "new_price")
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductDeliveryInline]


admin.site.register(Product, ProductAdmin)