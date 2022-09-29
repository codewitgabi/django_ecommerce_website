from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import uuid


def shop(request):
	
	q = request.GET.get("q") if request.GET.get("q") != None else ""
	products = Product.objects.filter(
		Q(name__icontains= q) |
		Q(category__name__icontains= q)
	).order_by("?")
	categories = Category.objects.all()
	context = {
		"products": products,
		"categories": categories
	}
	return render(request, "products/shop.html", context)
	

@login_required(login_url= "accounts:login")
def cart(request):
	try:
		if request.user.is_authenticated:
			order, created = Order.objects.get_or_create(customer= request.user, complete= False)
			products = order.orderitem_set.all()
			cart_price_total = order.price_total
		else:
			products = ""
			cart_price_total = 0
		categories = Category.objects.all()
		context = {
			"products": products,
			"cart_price_total": cart_price_total,
			"categories": categories,
		}
	except:
		pass
		context = {
			"products": "",
			"cart_price_total": "",
			"categories": ""
		}
	return render(request, "products/cart.html", context)
	

@login_required(login_url= "accounts:login")
def checkout(request):
	try:
		if request.user.is_authenticated:
			order, created = Order.objects.get_or_create(customer= request.user, complete= False)
			products = order.orderitem_set.all()
			cart_price_total = order.price_total
		else:
			products = ""
			cart_price_total = 0
		categories = Category.objects.all()
		context = {
			"cart_price_total": cart_price_total,
			"categories": categories,
		}
	except:
		pass
		context = {
			"cart_price_total": "",
			"categories": "",
		}
	return render(request, "products/checkout.html", context)
	
	
def updateCartItem(request):
	try:
		data = json.loads(request.body)
		product_id = data.get("product_id")
		action = data.get("action")
		
		order, created = Order.objects.get_or_create(customer= request.user, complete= False)
		product, created = order.orderitem_set.get_or_create(product_id= int(product_id))
		
		if action == "add":
			product.quantity += 1
			product.save()
			
		if action == "remove":
			product.quantity -= 1
			product.save()
			
		if product.quantity <= 0:
			product.delete()
	except:
		pass
	
	return JsonResponse("Sent", safe= False)
	
	
def getCartTotal(request):
	cart_total = 0
	try:
		if request.user.is_authenticated:
			order, created = Order.objects.get_or_create(customer= request.user, complete= False)
			cart_total = order.cart_total
		else:
			cart_total = 0
			return JsonResponse(cart_total, safe= False)
	except:
		order_lists = Order.objects.filter(customer= request.user, complete= False)
		if order_lists:
			for item in order_lists:
				item.delete()
		return JsonResponse(cart_total, safe= False)
	return JsonResponse(cart_total, safe= False)
		
	
def processOrder(request):
	try:
		data = json.loads(request.body)
		country = data.get("country")
		city = data.get("city")
		address = data.get("address")
		zipcode = data.get("zipcode")
		telephone = data.get("tel")
		price = data.get("cart_price_total")
		transaction_id = uuid.uuid4()
		
		order, created = Order.objects.get_or_create(customer= request.user, complete= False)
		order.transaction_id = transaction_id
	
		if price == str(order.price_total):
			order.complete = True
				
			order.save()
				
			ShippingInfo.objects.create(
				customer= request.user,
				order= order,
				address= address,
				city= city,
				country= country,
				zipcode= zipcode,
				telephone= telephone
			)
	except:
		pass
	
	return JsonResponse("Payment Was Successful!!!", safe= False) 
	
	
def getCartProducts(request):
	try:
		products = []
		products_price_total = "0.00"
		if  request.user.is_authenticated:
			order, created = Order.objects.get_or_create(customer= request.user, complete= False)
			items = order.orderitem_set.all()
	
			for col in list(items.values()):
				quantity = col.get("quantity")
				image = Product.objects.get(id= col.get("product_id")).image.url
				price = OrderItem.objects.get(id= col.get("id")).product_price_cumm
				price = str(price)
				products_price_total = str(order.price_total)
				product_id = col.get("product_id")
				products.append({"id": product_id, "quantity": quantity, "image": image, "price": price})
			
		else:
			products_price_total = "0.00"
	except:
		pass
	
	return JsonResponse({"products": products, "products_price_total": products_price_total}, safe= False) 