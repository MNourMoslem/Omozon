from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SellerUser, BuyerUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'account_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('account_type',)}),
    )

@admin.register(SellerUser)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'seller_rating', 'total_products']
    search_fields = ['business_name', 'user__username']

@admin.register(BuyerUser)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

admin.site.register(CustomUser, CustomUserAdmin)
