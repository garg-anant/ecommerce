from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import RegisterUser
from .models import ProfileUser, LedgerTable
from django.contrib.auth import authenticate, login, logout
import xlrd
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.
def index(request):
	if request.method == 'POST':
		user_name = request.POST.get('username')
		user_password = request.POST.get('password')
		# user = ProfileUser.objects.filter(username=user_name, password=user_password).exists()
		user = authenticate(username=user_name, password=user_password)
		if user is not None:
			if user.is_vendor:
				login(request, user)
				return HttpResponseRedirect(reverse('ecom:main'))
			else:
				login(request, user)
				return HttpResponseRedirect(reverse('ecom:main'))			

	return render(request, 'ecom/index.html',{})


def register(request):
	form = RegisterUser(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			data = form.save()
			data.set_password(request.POST.get('password'))
			data.save()
			# print (form.cleaneddata['name'])
			if form['is_vendor'].value():
				return HttpResponseRedirect(reverse('ecom:main'))
			else:
				return HttpResponseRedirect(reverse('ecom:main'))

		return render(request, 'ecom/register.html', {'form':form})
	return render(request, 'ecom/register.html', {'form':form})	


def main(request):

	if not request.user.is_authenticated:
		return render(request, 'ecom/index.html', {})
	else:
		
		if request.user.is_vendor:
			ctx2 = {}
			userid = request.user.id
			username = request.user.username

			if request.method == 'POST':
				
				ctx1 = {}
				# print (userid, "I AM HERE")
				myfile = request.FILES['myfile']
				fs = FileSystemStorage()
				filename = fs.save(myfile.name, myfile)
				path = '/home/anant/Desktop/ecommerce/src/comm/media/'+filename
				# print(path)
				# os.system('mv '+path+' home/anant/Desktop/project/myvenv/media/vendor.xlsx')
				# path = '/home/anant/Desktop/project/myvenv/media/vendor.xlsx'
				list_products = LedgerTable.objects.filter(profileuser_id = userid)

				list_of_products = []

				for obj in list_products:
					list_of_products.append(obj.product_name) 	
					list_of_products.append(obj.profileuser)
					list_of_products.append(obj.product_colour)
					list_of_products.append(obj.product_ram)
					list_of_products.append(obj.product_memory)

				wb = xlrd.open_workbook(path)
				first_sheet = wb.sheet_by_index(0)
				n_rows = first_sheet.nrows
				# n_cols = first_sheet.ncols
				# print(n_cols,'errrrr')
				for i in range(1,n_rows):
					if (first_sheet.cell(i,0).value in list_of_products) and (first_sheet.cell(i,1).value in list_of_products) and (first_sheet.cell(i,4).value in list_of_products) and (first_sheet.cell(i,5).value in list_of_products):
						if userid == list_of_products.index(first_sheet.cell(i,0).value)+1 and userid == list_of_products.index(first_sheet.cell(i,1).value)-1 and userid == list_of_products.index(first_sheet.cell(i,4).value)-2 and userid == list_of_products.index(first_sheet.cell(i,5).value)-3:
							reccurring_product = LedgerTable.objects.get(product_name=row[0], profileuser_id=userid)
							reccurring_product.product_colour = first_sheet.cell(i,1).value
							reccurring_product.product_screen_size = first_sheet.cell(i,2).value
							reccurring_product.product_os = first_sheet.cell(i,3).value
							reccurring_product.product_ram = first_sheet.cell(i,4).value
							reccurring_product.product_memory = first_sheet.cell(i,5).value
							reccurring_product.product_price = first_sheet.cell(i,6).value
							reccurring_product.save()
					else:
						create_ledger = LedgerTable.objects.create(
							product_name = first_sheet.cell(i,0).value,
							product_colour = first_sheet.cell(i,1).value,
							product_screen_size = first_sheet.cell(i,2).value,
							product_os = first_sheet.cell(i,3).value,
							product_ram = first_sheet.cell(i,4).value,
							product_memory = first_sheet.cell(i,5).value,
							product_price = first_sheet.cell(i,6).value,
							# profileuser = userid
							profileuser_id = request.user.id
							)			
												
				os.system('rm ' + path)

				list_products = LedgerTable.objects.filter(profileuser_id = userid)
				print(userid)
				print(list_products)

				ctx1 = {
				'username': username,
				'check_vendor' : request.user.is_vendor,
				'list_products' : list_products
				}
				return render(request, 'ecom/main.html', ctx1)
			
			list_products = LedgerTable.objects.filter(profileuser_id = userid)
			ctx1 = {
				'username' : username,
				'check_vendor' : request.user.is_vendor,
				'list_products' : list_products
				}
			return render(request, 'ecom/main.html', ctx1)
		
		#code for viewers to display maximum priced each phone
		all_products = LedgerTable.objects.all().order_by('-product_price')
		new_all_products = []
		for i in all_products:
			if i.product_name not in new_all_products:
				new_all_products.append(i.id)
				new_all_products.append(i.product_name)
		
		all_products = []
		for j in new_all_products[::2]:
			all_products.append(LedgerTable.objects.get(id=j))
			
		ctx2 = {
			'username' : request.user.username,
			'all_products' : all_products,
			'check_vendor' : request.user.is_vendor
		}
		return render(request, 'ecom/main.html', ctx2)


def change_price(request, ledger_id):
	
	if request.method == 'POST':
		userid = request.user.id
		a = LedgerTable.objects.get(id=ledger_id)
		name = a.product_name
		new_price = request.POST.get(name)
		a.product_price = new_price
		a.save()
		list_products = LedgerTable.objects.filter(profileuser_id = userid)
		ctx = {
			'check_vendor': request.user.is_vendor,
			'username':request.user.username,
			'list_products':list_products,

		}
		return render(request, 'ecom/main.html', ctx)
	ctx={}
	list_products = LedgerTable.objects.all()
	ctx = {
			'check_vendor': request.user.is_vendor,
			'username':request.user.username,
			'list_products':list_products,

		} 
	return render(request, 'ecom/main.html', ctx)

def logout_func(request):
	logout(request)
	return HttpResponseRedirect(reverse('ecom:index'))

		
