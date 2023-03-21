from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_editable = ('name', 'description', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'price')
    list_editable = ('user', 'price')


@admin.register(Cart)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_editable = ('user',)


@admin.register(UserCustom)
class UserCustomAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff')
    list_editable = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('email', 'username', 'first_name', 'last_name', 'is_staff')

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'username',
                    'is_staff'),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
