from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at", "product_name")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "id")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
