from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Number of empty rows to display for adding new items
    readonly_fields = ('get_total_price', 'get_product_name')
    fields = ('get_product_name', 'quantity', 'get_total_price')
    verbose_name_plural = "Cart Items"

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'coupon', 'get_total_price')
    list_filter = ('created_at', 'coupon')
    search_fields = ('user__username', 'coupon__code')
    inlines = [CartItemInline]
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'get_user', 'get_product_name', 'quantity', 'get_total_price')
    list_filter = ('cart__user', 'product')
    search_fields = ('cart__user__username', 'product__name')

    readonly_fields = ('get_product_name', 'get_total_price')

    def get_user(self, obj):
        return obj.cart.user.username
    get_user.short_description = 'User'

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'
