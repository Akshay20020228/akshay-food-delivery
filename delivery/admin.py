from django.contrib import admin

# Register your models here.
from .models import FoodItem


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "available")
    search_fields = ("name",)
    list_filter = ("available",)

from .models import Order

admin.site.register(Order)
