from django.db import models
from accounts.models import User
	
	
class Product(models.Model):
	name = models.CharField(max_length= 100)
	price = models.DecimalField(max_digits= 10, decimal_places= 2, default= 0)
	image = models.ImageField(upload_to= "products_image/")
	category = models.ForeignKey("Category", on_delete= models.SET_NULL, null= True, blank= True)
	
	
	def __str__(self):
		return self.name
		
		
class Category(models.Model):
	name = models.CharField(max_length= 30)
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name_plural = "Categories"
		
		
class Order(models.Model):
	customer = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, blank= True)
	date_created = models.DateTimeField(auto_now= True)
	complete = models.BooleanField(default= False)
	transaction_id = models.CharField(max_length= 36)
	
	@property
	def cart_total(self):
		total = 0
		for item in self.orderitem_set.all():
			total += item.quantity
		return total
		
	@property
	def price_total(self):
		price = 0
		for item in self.orderitem_set.all():
			price += (item.quantity * item.product.price)
		return price
	
	def __str__(self):
		return str(self.id)
		
		
class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete= models.SET_NULL, null= True, blank= True)
	product = models.ForeignKey(Product, on_delete= models.SET_NULL, null= True, blank= True)
	quantity = models.IntegerField(default= 0)
	
	@property
	def product_price_cumm(self):
		return self.quantity * self.product.price
		
	
class ShippingInfo(models.Model):
	customer = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, blank= True)
	order = models.ForeignKey(Order, on_delete= models.SET_NULL, null= True, blank= True)
	country = models.CharField(max_length= 100, null= True)
	city = models.CharField(max_length= 100, null= True)
	address = models.CharField(max_length= 800, null= True)
	zipcode = models.CharField(max_length= 300)
	telephone = models.CharField(max_length= 15)
	
	def __str__(self):
		return self.country
				
		
	class Meta:
		verbose_name_plural = "ShippingInfo"