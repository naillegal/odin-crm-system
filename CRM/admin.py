from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Feature, Customer, PriceOffer, SalesContract, CustomerProduct, PriceOfferProduct, Design3D

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


@admin.register(Design3D)
class Design3DAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'image_preview')
    search_fields = ('title',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: contain;" />',
                obj.image.url,
            )
        return "Şəkil yoxdur"

    image_preview.short_description = "Şəkil Ön Baxış"


class PriceOfferProductInline(admin.TabularInline):
    model = PriceOfferProduct
    extra = 1
    verbose_name = "Məhsul"
    verbose_name_plural = "Məhsullar"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "design_3d":
            kwargs["empty_label"] = "Yoxdur"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Customer admin


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_number',
                    'customer_code', 'created_at')
    list_filter = ('created_at', 'full_name')
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
    list_display = ('customer', 'system_name', 'payment_type',
                    'views_count', 'created_at')
    list_filter = ('payment_type', 'created_at',
                   'glass_thickness', 'profile_color')
    search_fields = ('system_name', 'customer__customer_code',
                     'customer__full_name')
    readonly_fields = ('created_at', 'views_count')
