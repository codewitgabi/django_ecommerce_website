from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import PhoneNumberValidator


class User(AbstractUser):
	username = models.CharField(max_length= 100, blank= True, null= True)
	email = models.EmailField(unique= True)
	
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]
	
	def __str__(self):
		return self.username