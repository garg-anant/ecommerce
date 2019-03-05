from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.conf import settings


class ProfileUser(AbstractUser):
	name = models.CharField(max_length=250)
	mobile = models.CharField(max_length=10, null=True, blank=True)
	email = models.CharField(max_length=100)
	is_vendor = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class LedgerTable(models.Model):
	product_name = models.CharField(max_length=50)
	product_colour = models.CharField(max_length=50)
	product_screen_size = models.CharField(max_length=10)
	product_os = models.CharField(max_length=50)
	product_ram = models.CharField(max_length=10)
	product_memory = models.CharField(max_length=10)
	product_price = models.PositiveIntegerField(default=0)
	profileuser = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.product_name
