from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Pin, PinSize, SellerSlider, MyCart, PinSet, category, Orders, PinSetOrders
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SellerInfo ,SellerRegisterForm, SellerAddressForm, UpdateSellerDetailForm, UpdateSellerAccountDetailForm
from buyer.forms import UserUpdateForm
from django.contrib.auth.decorators import login_required
from math import ceil
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

#This is view of Index Page of Seller in which we Display Whole Sale pins
@login_required
def index(request):
	if request.user.is_superuser or request.user.is_staff:
		allProds = []
		catprods = Pin.objects.values('category', 'pin_id')
		cats = {item['category'] for item in catprods}
		for cat in cats:
			prod = Pin.objects.filter(category=cat)
			n = len(prod)
			nSlides = n // 6 + ceil((n / 6) - (n // 6))
			allProds.append([prod, range(1, nSlides), nSlides])
		params = {
				'allPins':allProds,
				'pin': Pin.objects.all()[::-1][:4],
				'sliders':SellerSlider.objects.all(),
				'trending': Pin.objects.all(),
				'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
				}
		print(request)
		return render(request, 'seller/index.html', params)
	else:
		return redirect("/")

# This is View of Dashboard in which we display all orders of the seller and ther status
@login_required
def dashboard(request):
	if request.user.is_superuser :
		if request.method == 'GET':
			odrr = request.GET.get('odrr')
			st = request.GET.get('st')
			if st == 'Cancel':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Cancel'
				o.save()
			if st == 'Accepted':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Accepted'
				o.save()
			if st == 'Packed':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Packed'
				o.save()
			if st == 'Delivered':
				o = Orders.objects.filter(order_id=odrr).first()
				o.status = 'Delivered'
				o.save()
		ordr = [i for i in Orders.objects.filter(seller=request.user) if i.status != 'Cancel' and i.status != 'On The Way' and i.status != 'Delivered'][::-1]
		params = {
				'orders':ordr,
				'dorders': [i for i in Orders.objects.filter(seller=request.user) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'][::-1],
				'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
				}
		return render(request, 'seller/dashboard.html', params)
	else:
		return redirect("/")

# This is add to cart view of Seller means Whole Sale pins
@login_required
def add_to_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.pin_id for i in cart_prods]
	if request.method == 'GET':
		pin_id = request.GET['pin_id']
		if pin_id in card_prods_id:
			cart_prods[card_prods_id.index(pin_id)].number += Pin.objects.filter(pin_id=pin_id)[0].quantity
			cart_prods[card_prods_id.index(pin_id)].save()
			return HttpResponse(len(cart_prods))

		else:
			MyCart(user = request.user, pin_id = pin_id, number = Pin.objects.filter(pin_id=pin_id)[0].quantity).save()
			return HttpResponse(len(cart_prods)+1)
	else:
		return HttpResponse("")

# This is view for Increasing Quantity of any pin in Cart
@login_required
def plus_element_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.pin_id for i in cart_prods]
	if request.method == 'GET':
		pin_id = request.GET['pin_id']
		if pin_id in card_prods_id:
			cart_prods[card_prods_id.index(pin_id)].number += Pin.objects.filter(pin_id=pin_id)[0].quantity
			cart_prods[card_prods_id.index(pin_id)].save()
			subtotal = 0.0
			delev = 0.0
			cart_prods2 = [p for p in MyCart.objects.all() if p.user == request.user]
			for p in cart_prods2:
				subtotal += p.number * Pin.objects.filter(pin_id=p.pin_id)[0].price
			tax = subtotal*5/100
			datas = {
				'num':MyCart.objects.filter(user=request.user,pin_id=pin_id)[0].number,
				'tax':tax,
				'subtotal':subtotal,
				'delev' : delev,
				'total':subtotal+tax+delev,
				}
			return JsonResponse(datas)
	else:
		return HttpResponse("")

# This is view for Decreasing Quantity of any pin in Cart
@login_required
def minus_element_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.pin_id for i in cart_prods]
	if request.method == 'GET':
		prod_id = request.GET['pin_id']
		if prod_id in card_prods_id:
			cart_prods[card_prods_id.index(prod_id)].number -= Pin.objects.filter(pin_id=prod_id)[0].quantity
			cart_prods[card_prods_id.index(prod_id)].save()
			subtotal = 0.0
			delev = 0.0
			cart_prods2 = [p for p in MyCart.objects.all() if p.user == request.user]
			for p in cart_prods2:
				subtotal += p.number * Pin.objects.filter(pin_id=p.pin_id)[0].price
			tax = subtotal*5/100
			datas = {
				'num':MyCart.objects.filter(user=request.user,pin_id=prod_id)[0].number,
				'tax':tax,
				'subtotal':subtotal,
				'delev' : delev,
				'total':subtotal+tax+delev,
				}
			return JsonResponse(datas)
	else:
		return HttpResponse("")

# This is view for Deleting a pin from Cart
@login_required
def delete_from_cart(request):
	cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
	card_prods_id =[i.pin_id for i in cart_prods]
	if request.method == 'GET':
		pin_id = request.GET['pin_id']
		if pin_id in card_prods_id:
			cart_prods[card_prods_id.index(pin_id)].delete()
			subtotal = 0.0
			delev = 0.0
			cart_prods2 = [p for p in MyCart.objects.all() if p.user == request.user]
			for p in cart_prods2:
				subtotal += p.number * Pin.objects.filter(pin_id=p.pin_id)[0].price
			tax = subtotal*5/100
			datas = {
				'len':len(cart_prods2),
				'tax':tax,
				'subtotal':subtotal,
				'delev' : delev,
				'total':subtotal+tax+delev,
				}
			return JsonResponse(datas)
	else:
		return HttpResponse("")

# This view for Display a Single pin 
@login_required
def pinView(request, pin_id):
	if request.user.is_superuser or request.user.is_staff:
		params = {
			'pin': Pin.objects.filter(pin_id = pin_id)[0],
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
		}
		return render(request, 'seller/view_pins.html', params)
	else:
		return redirect("/")

# This is View of Display all pins of a perticular category
@login_required
def view_all(request, catg):
	if request.user.is_superuser or request.user.is_staff:
		params = {
			'pin':[i for i in Pin.objects.all() if str(i.category) == catg],
			'catg':catg,
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			}
		return render(request, 'seller/view_all.html', params)
	else:
		return redirect("/")

# seller cart view
@login_required
def mycart(request):
	if request.user.is_superuser or request.user.is_staff:
		allProds = []
		subtotal = 0.0
		delev = 0.0
		cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
		for p in cart_prods:
			subtotal += p.number * Pin.objects.filter(pin_id=p.pin_id)[0].price
		tax = subtotal*5/100

		for cprod in cart_prods:
			prod = Pin.objects.filter(pin_id=cprod.pin_id)[0]
			allProds.append([cprod, prod])
		params = {
					'allPins':allProds,
					'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
					'total':subtotal+tax+delev,
					'subtotal':subtotal,
					'tax':tax,
					'delev':delev,
				}
		return render(request,'seller/cart.html', params)
	else:
		return redirect("/")

# seller checkout view means for whole sale pins
def checkout(request):
	if request.user.is_superuser or request.user.is_staff:
		allProds = []
		cart_prods = [p for p in MyCart.objects.all() if p.user == request.user]
		for cprod in cart_prods:
			prod = Pin.objects.filter(pin_id=cprod.pin_id)[0]
			allProds.append([cprod, prod])
		if request.method == 'POST':
			address_form = SellerAddressForm(request.POST, instance=request.user.sellerdetail)
			if address_form.is_valid():
				address_form.save()
				for item in cart_prods:
					if Pin.objects.all().last():
						order_id = 'WSPOrder'+str((Pin.objects.all().last().pk)+1)
					else:
						order_id = 'WSPOrder001'
					pin1 = item.pin_id+'|'+str(item.number)+','
					Pin(order_id=order_id,user=request.user,pins=pin1).save()
					item.delete()
				return redirect('seller_orders')
		else:
			address_form = SellerAddressForm(instance=request.user.sellerdetail)

		subtotal = 0.0
		delev = 0.0
		for p in cart_prods:
			subtotal += p.number * Pin.objects.filter(pin_id=p.pin_id)[0].price
		tax = subtotal*5/100
		params = {
				'allPins':allProds,
				'cart_element_no' : len(cart_prods),
				'address_form': address_form,
				'total':subtotal+tax+delev,
			}
		return render(request, 'seller/checkout.html', params)
	else:
		return redirect("/")

# Orders of Seller (Whole sale pin)
def MyOrders(request):
	if request.method == 'POST':
		order_id = request.POST.get('order_id')
		o = Pin.objects.filter(order_id=order_id)[0]
		o.status = 'Cancel'
		o.save()
	params = {
		'orders': [i for i in Pin.objects.all() if i.user == request.user and i.status != 'Delivered' and i.status != 'Cancel'],
		'delivered': [i for i in Pin.objects.all() if i.user == request.user and i.status == 'Delivered'],
		'cancel': [i for i in Pin.objects.all() if i.user == request.user and i.status == 'Cancel'],

	}
	return render(request,'seller/myorders.html', params)

# for adding a new pin by seller 
@login_required
def add_pin(request):
	if request.user.is_superuser or request.user.is_staff:
		if request.method == 'POST':
			pin_name = request.POST.get('pin_name')
			desc = request.POST.get('desc')
			cat = request.POST.get('category')
			price = request.POST.get('price')
			price_not = request.POST.get('price_not')
			if Pin.objects.all():
				prod_id2 = 'pr'+hex(Pin.objects.all().last().pin_id+1)
			else:
				prod_id2 = 'pr'+hex(0)
			image1 = request.FILES.get("image1")
			image2 = request.FILES.get("image2")
			image3 = request.FILES.get("image3")
			image4 = request.FILES.get("image4")
			i=1
			sizes=[]
			# while i <= size_no:
			# 	if request.POST.get(f'size{i}'):
			# 		sizes.append([request.POST.get(f'size{i}'),int(request.POST.get(f'quantity{i}'))])
			# 	i+=1
			Pin(pin_id2=prod_id2,shop=request.user,pin_name=pin_name,category=category.objects.get(id=int(cat)),price=price,price_not=price_not,desc=desc,image1=image1).save()
			p = Pin.objects.filter(pin_id2=prod_id2)[0]
			if image2:
				p.image2=image2
			if image3:
				p.image3=image3
			if image4:
				p.image4=image4
			p.save()
			for siz in sizes:
				PinSize(pin=p,quantity=siz[1]).save()
			messages.success(request, f'pin Added !')
		prod = [p for p in Pin.objects.all() if p.shop == request.user]

		if request.method == 'GET':
			pro_id = request.GET.get('pin_id', 0)
			del_prod = [p.pin_id for p in Pin.objects.all() if p.shop == request.user]
			if int(pro_id) in del_prod:
				Pin.objects.filter(pin_id=int(pro_id))[0].delete()
				messages.success(request, f'The pin of id {pro_id} is deleted !')
				return redirect('/seller/add_pin/')

		subcat=[]
		for cat in category.objects.all():
			x = cat.sub_Categories.split(',')
			x.insert(0, cat)
			subcat.append(x)
		params = {
			'pin':prod[::-1][0:20],
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			'subcat':subcat,
			}
		return render(request, 'seller/add_pin.html',params)
	else:
		return redirect("/")

# it will display all pins of a seller
@login_required
def view_pins(request):
	if request.user.is_superuser or request.user.is_staff:
		prod = [p for p in Pin.objects.all() if p.shop == request.user]

		if request.method == 'GET':
			pro_id = request.GET.get('pin_id')
			if pro_id:
				del_prod = [p.pin_id for p in Pin.objects.all() if p.shop == request.user]
				if int(pro_id) in del_prod:
					Pin.objects.filter(pin_id=int(pro_id))[0].delete()
					messages.success(request, f'The pin of id {pro_id} is deleted !')
					return redirect('/seller/view_pins/')

		params = {
			'pin': prod[::-1],
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			}
		return render(request, 'seller/view_pins.html',params)
	else:
		return redirect("/")

# Signup for Seller
def seller_signup(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			form = SellerRegisterForm(request.POST)
			if form.is_valid():
				form.save();
				username = form.cleaned_data.get('username')
				shop = form.cleaned_data.get('shop')
				usr = User.objects.filter(username=username).first()
				usr.is_staff=True
				usr.save()
				if username.isdigit():
					SellerInfo(user=usr,mobile=username,seller_Name=shop).save()
				else:
					usr.email = username
					usr.save()
					SellerInfo(user=usr,seller_Name=shop).save()
				messages.success(request, f'Account is Created for {username}')
				return redirect('login')
		else:
			form = SellerRegisterForm()
	return render(request, 'seller/seller_signup.html', {'form':form, 'title':'Become a Seller'})

# Seller Account Settings
@login_required
def account_settings(request):
	if request.user.is_superuser or request.user.is_staff:
		if request.method == 'POST':
			#User Details Update
			s_form = UpdateSellerDetailForm(request.POST, request.FILES, instance=request.user.Sellerdetail)
			u_form = UserUpdateForm(request.POST, instance=request.user)
			if s_form.is_valid() and u_form.is_valid():
				s_form.save()
				u_form.save()
				messages.success(request, f'Your Account has been Updated!')
				return redirect("seller_account_settings")

			#Change Password
			pass_change_form = PasswordChangeForm(request.user, request.POST)
			if pass_change_form.is_valid():
				user = pass_change_form.save()
				update_session_auth_hash(request, user)  # Important!
				messages.success(request, 'Your password was successfully updated!')
				return redirect('seller_account_settings')
			else:
				messages.error(request, 'Please correct the error below.')

			#Account Settings
			acc_form = UpdateSellerAccountDetailForm(request.POST, request.FILES, instance=request.user.Sellerdetail)
			if acc_form.is_valid():
				acc_form.save()
				messages.success(request, f'Account Settings has been Updated!')
				return redirect("seller_account_settings")

		else:
			s_form = UpdateSellerDetailForm(instance=request.user.sellerdetail)
			u_form = UserUpdateForm(instance=request.user)
			acc_form = UpdateSellerAccountDetailForm(instance=request.user.sellerdetail)
			pass_change_form = PasswordChangeForm(request.user)
		detl = {
			'u_form':u_form,
			's_form':s_form,
			'pass_change_form':pass_change_form,
			'acc_form':acc_form,
			'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
			'title':'User Account Settings',
			}
		return render(request, 'seller/account_settings.html', detl)
	else:
		return redirect("/")

# This is a part of admin view in which all ordered pins will display with address
def admin2(request):
	if request.user.is_superuser:
		ordr = [i for i in Orders.objects.all() if i.status != 'Cancel' and i.status != 'On The Way' and i.status != 'Delivered'][::-1]
		params = {
				'orders':ordr,
				'dorders': [i for i in Orders.objects.filter(seller=request.user) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'],
				'cart_element_no' : len([p for p in MyCart.objects.all() if p.user == request.user]),
				}
		return render(request, 'seller/admin2.html', params)
	else:
		return redirect("/")
