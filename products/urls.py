from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
	path("", views.shop, name= "shop"),
	path("cart/", views.cart, name= "cart"),
	path("checkout/", views.checkout, name= "checkout"),
	
	#API urls
	path("updateCartItem/", views.updateCartItem, name= "updateCartItem"),
	path("getCartTotal/", views.getCartTotal, name= "getCartTotal"),
	path("processOrder/", views.processOrder, name= "processOrder"),
	path("getCartProducts", views.getCartProducts, name= "getCartProducts"),
]