# from django.contrib import admin
# from .models import DeliveryOption, DeliveryAddress, Delivery



# @admin.register(DeliveryOption)
# class DeliveryOptionAdmin(admin.ModelAdmin):
#     """
#     Admin configuration for the DeliveryOption model.
#     """
#     list_display = ['id', 'name', 'delivery_fee', 'estimated_time']
#     list_filter = ['name']
#     search_fields = ['name', 'description']
#     ordering = ['id']
#     filter_horizontal = ['zone']  # For managing the ManyToManyField


# @admin.register(DeliveryAddress)
# class DeliveryAddressAdmin(admin.ModelAdmin):
#     """
#     Admin configuration for the DeliveryAddress model.
#     """
#     list_display = [
#         'id', 'user', 'full_name', 'phone_number', 'address_line_1',
#         'city', 'postal_code', 'country', 'zone'
#     ]
#     list_filter = ['city', 'zone', 'country']
#     search_fields = [
#         'full_name', 'phone_number', 'address_line_1', 'city', 'postal_code'
#     ]
#     ordering = ['id']


# @admin.register(Delivery)
# class DeliveryAdmin(admin.ModelAdmin):
#     """
#     Admin configuration for the Delivery model.
#     """
#     list_display = [
#         'id', 'user', 'delivery_option', 'delivery_address',
#         'status', 'tracking_number', 'created_at', 'updated_at'
#     ]
#     list_filter = ['status', 'delivery_option', 'created_at']
#     search_fields = ['tracking_number', 'user__username']
#     ordering = ['id']
#     readonly_fields = ['created_at', 'updated_at']  # Read-only fields
