from django.contrib import admin
from .models import Product, Feature, Customer, PriceOffer, SalesContract, CustomerProduct, PriceOfferProduct

# Feature admin
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

# Inline for CustomerProduct inside CustomerAdmin
class CustomerProductInline(admin.TabularInline):
    model = CustomerProduct
    extra = 1
    verbose_name = "Məhsul"
    verbose_name_plural = "Məhsullar"

# Inline for PriceOfferProduct inside PriceOfferAdmin
class PriceOfferProductInline(admin.TabularInline):
    model = PriceOfferProduct
    extra = 1
    verbose_name = "Məhsul"
    verbose_name_plural = "Məhsullar"

# Customer admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_number', 'initial_price_offer', 'inquiry_method', 'customer_code', 'created_at')
    list_filter = ('created_at', 'inquiry_method')
    search_fields = ('full_name', 'contact_number', 'customer_code')
    readonly_fields = ('created_at', 'customer_code')

    inlines = [CustomerProductInline]

# PriceOffer admin
@admin.register(PriceOffer)
class PriceOfferAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'views_count')
    list_filter = ('created_at', 'views_count')
    search_fields = ('customer__full_name', 'customer__customer_code')
    readonly_fields = ('created_at', 'views_count')

    inlines = [PriceOfferProductInline]

# SalesContract admin
@admin.register(SalesContract)
class SalesContractAdmin(admin.ModelAdmin):
    list_display = ('customer', 'system_name', 'payment_type', 'views_count', 'created_at')
    list_filter = ('payment_type', 'created_at', 'glass_thickness', 'profile_color')
    search_fields = ('system_name', 'customer__customer_code', 'customer__full_name')
    readonly_fields = ('created_at', 'views_count')
