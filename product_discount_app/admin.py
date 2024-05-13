# admin.py
from django.contrib import admin
from .models import Discount, Category, Product

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount_type', 'amount', 'start_date', 'end_date', 'start_time', 'end_time')
    list_filter = ('type', 'amount_type')
    search_fields = ('type', 'amount_type')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'discount')
    list_filter = ('category', 'discount')
    search_fields = ('name', 'category__name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'discount')
