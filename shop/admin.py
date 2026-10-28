from django.contrib import admin
from .models import Category, Order, OrderItem, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "featured")
    list_filter = ("category", "featured")
    list_editable = ("price", "stock", "featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "name", "size", "price", "qty")
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "city", "total", "status", "created")
    list_filter = ("status", "created")
    list_editable = ("status",)
    search_fields = ("full_name", "email", "phone")
    inlines = [ItemInline]
