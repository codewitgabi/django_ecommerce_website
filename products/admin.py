from django.contrib import admin
from .models import *

	
class ProductAdmin(admin.ModelAdmin):
	list_display = ["name", "price"]
	list_filter = ["name", "price"]
	search_fields = ["name"]
	
	
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	
	
class OrderAdmin(admin.ModelAdmin):
	list_display = ["customer", "complete"]
	list_filter = ["complete"]
	inlines = [OrderItemInline]


class ShippingInfoAdmin(admin.ModelAdmin):
	list_display = ["customer", "country", "city", "telephone", ]
	list_filter = ["city", "country"]
	search_fields = ["city", "country"]
	
	
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name"]
	search_fields = ["name"]
	
	
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingInfo, ShippingInfoAdmin)
admin.site.register(Category, CategoryAdmin)