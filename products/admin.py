from django.contrib import admin
from .models import Product, Category, ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'stock')  # Columns in the list view
    list_filter = ('category', 'price')  # Filters in the sidebar
    search_fields = ('name', 'slug', 'description')  # Searchable fields
    ordering = ('-price',)  # Default ordering
    list_editable = ('price', 'stock')  # Inline editable fields
    readonly_fields = ('uuid',)  # Non-editable fields in the admin form
    fieldsets = (  # Organizing fields in the form view
        ("Product Information", {
            'fields': ('uuid', 'slug', 'name', 'category', 'description')
        }),
        ("Inventory", {
            'fields': ('price', 'stock', 'image')
        }),
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)