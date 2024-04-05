from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class SellerInfo(models.Model):
	SEX_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
	STATE_CHOICES = (
		("Alabama",'Alabama'),
		("Alaska",'Alaska'),
		("Arizona",'Arizona'),
		("Arkansas",'Arkansas'),
		("California",'California'),
		("Colorado",'Colorado'),
		("Connecticut",'Connecticut'),
		("Delaware",'Delaware'),
		("Florida",'Florida'),
		("Georgia",'Georgia'),
		("Hawaii",'Hawaii'),
		("Idaho",'Idaho'),
		("Illinois",'Illinois'),
		("Indiana",'Indiana'),
		("Iowa",'Iowa'),
		("Kansas",'Kansas'),
		("Kentucky",'Kentucky'),
		("Louisiana",'Louisiana'),
		("ihearte",'ihearte'),
		("Maryland",'Maryland'),
		("Massachusetts",'Massachusetts'),
		("Michigan",'Michigan'),
		("Minnesota",'Minnesota'),
		("Mississippi",'Mississippi'),
		("Missouri",'Missouri'),
		("Montana",'Montana'),
		("Nebraska",'Nebraska'),
		("Nevada",'Nevada'),
		("New Hampshire",'New Hampshire'),
		("New Jersey",'New Jersey'),
		("New Mexico",'New Mexico'),
		("New York",'New York'),
		("North Carolina",'North Carolina'),
		("North Dakota",'North Dakota'),
		("Ohio",'Ohio'),
		("Oklahoma",'Oklahoma'),
        ("Oregon",'Oregon'),
		("Pennsylvania",'Pennsylvania'),
		("Rhode Island",'Rhode Island'),
		("South Carolina",'South Carolina'),
		("South Dakota",'South Dakota'),
		("Tennessee",'Tennessee'),
		("Texas",'Texas'),
        ("Utah",'Utah'),
		("Vermont",'Vermont'),
        ("Virginia", 'Virginia'),
        ("Washington",'Washington'),
        ("West Virginia",'West Virginia'),
		("Wisconsin",'Wisconsin'),
        ("Wyoming", 'Wyoming'),
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
	photo = models.ImageField(default='default.png',upload_to='user_photos')
	mobile = models.CharField(max_length=10,null=True)
	seller_Name = models.CharField(max_length=500,null=True)
	alternate_mobile = models.CharField(max_length=10,null=True,blank=True)
	seller_Address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	account_Holder_Name = models.CharField(max_length=50, null=True)
	account_Number = models.CharField(max_length=20, null=True)
	ifsc_Code = models.CharField(max_length=11, null=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.photo.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.photo.path)

class SellerSlider(models.Model):
	name = models.CharField(max_length=50, default = "", null=True)
	image = models.ImageField(upload_to='seller_slider_img')
	url = models.CharField(max_length=200, default = "#", null=True)

	def __str__(self):
		return f'{self.name}'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)
		if img.height > 1024 or img.width > 1024:
			output_size = (1024, 1024)
			img.thumbnail(output_size)
			img.save(self.image.path)


class category(models.Model):
	name = models.CharField(max_length=50, default="")
	sub_Categories  = models.TextField(default="")
	def __str__(self):
		return f'{self.name}'

class Pin(models.Model):
	pin_id = models.BigAutoField(primary_key=True)
	pin_id2 = models.CharField(max_length=100,default='')
	shop = models.ForeignKey(User, on_delete=models.CASCADE,default='')
	pin_name = models.CharField(max_length=100)
	category = models.ForeignKey(category, default="", verbose_name="Category", on_delete=models.SET_DEFAULT, null=True)
	price = models.IntegerField(default=0)
	price_not = models.IntegerField(default=999)
	desc = models.TextField()
	pub_date = models.DateField(auto_now=True)
	image1 = models.ImageField(upload_to='pin/images', default="",null=True)
	image2 = models.ImageField(upload_to='pin/images', default="",null=True,blank=True)
	image3 = models.ImageField(upload_to='pin/images', default="",null=True,blank=True)
	image4 = models.ImageField(upload_to='pin/images', default="",null=True,blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img1 = Image.open(self.image1.path)
		if img1.height > 1500 or img1.width > 1500:
			output_size = (1500, 1500)
			img1.thumbnail(output_size)
			img1.save(self.image1.path)
		if self.image2:
			img2 = Image.open(self.image2.path)
			if img2.height > 1500 or img2.width > 1500:
				output_size = (1500, 1500)
				img2.thumbnail(output_size)
				img2.save(self.image2.path)

		if self.image3:
			img3 = Image.open(self.image3.path)
			if img3.height > 1500 or img3.width > 1500:
				output_size = (1500, 1500)
				img3.thumbnail(output_size)
				img3.save(self.image3.path)

		if self.image4:
			img4 = Image.open(self.image4.path)
			if img4.height > 1500 or img4.width > 1500:
				output_size = (1500, 1500)
				img4.thumbnail(output_size)
				img4.save(self.image4.path)

	def __str__(self):
		return f'{self.pin_id}'

class PinSize(models.Model):
	pin = models.ForeignKey(Pin,on_delete=models.CASCADE)
	# size = models.CharField(max_length=20)
	quantity = models.IntegerField(default=0, null=True)

class PinReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
	review = models.TextField()
	time = models.DateTimeField(auto_now=True)

class PinSet(models.Model):
	SEX_CHOICES = (("Male",'Male'),("Female",'Female'),("All",'All'))
	pinSet_id = models.BigAutoField(primary_key=True)
	pinSet_name = models.CharField(max_length=100)
	category = models.ForeignKey(category, default="", verbose_name="Category", on_delete=models.SET_DEFAULT)
	price = models.IntegerField(default=0)
	desc = models.TextField()
	#size = models.TextField(verbose_name='Size Avialabe(Separated by Comma)')
	color = models.TextField(verbose_name='Enter Color Separated by Comma')
	number_of_pins = models.IntegerField(default=0, null=True)
	pub_date = models.DateField(auto_now=True)
	image1 = models.ImageField(upload_to='pinSet/images', default="",null=True)
	image2 = models.ImageField(upload_to='pinSet/images', default="",null=True,blank=True)
	image3 = models.ImageField(upload_to='pinSet/images', default="",null=True,blank=True)
	image4 = models.ImageField(upload_to='pinSet/images', default="",null=True,blank=True)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img1 = Image.open(self.image1.path)
		if img1.height > 1500 or img1.width > 1500:
			output_size = (1500, 1500)
			img1.thumbnail(output_size)
			img1.save(self.image1.path)
		if self.image2:
			img2 = Image.open(self.image2.path)
			if img2.height > 1500 or img2.width > 1500:
				output_size = (1500, 1500)
				img2.thumbnail(output_size)
				img2.save(self.image2.path)

		if self.image3:
			img3 = Image.open(self.image3.path)
			if img3.height > 1500 or img3.width > 1500:
				output_size = (1500, 1500)
				img3.thumbnail(output_size)
				img3.save(self.image3.path)

		if self.image4:
			img4 = Image.open(self.image4.path)
			if img4.height > 1500 or img4.width > 1500:
				output_size = (1500, 1500)
				img4.thumbnail(output_size)
				img4.save(self.image4.path)

	def __str__(self):
		return f'{self.pinSet_id}'

class PinSetOrders(models.Model):
	STATUS_CHOICES = (("Accepted",'Accepted'),("Packed",'Packed'),("On The Way",'On The Way'),("Delivered",'Delivered'),("Cancel",'Cancel'))
	order_id = models.CharField(max_length=50,default='')
	user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
	pins = models.CharField(max_length=50)
	status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='')

class dow(models.Model):
	pin = models.OneToOneField(Pin, default="", verbose_name="Pin Id", on_delete=models.CASCADE, null=True)
	price = models.PositiveIntegerField()
	def __str__(self):
		return f'{self.pin}'

class trend(models.Model):
	pin = models.OneToOneField(Pin, default="", on_delete=models.CASCADE, null=True)
	number = models.PositiveIntegerField()
	def __str__(self):
		return f'{self.pin}'

class MyCart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pin_id = models.CharField(max_length=100)
	number = models.PositiveIntegerField(default=0)

class Orders(models.Model):
	STATUS_CHOICES = (("Accepted",'Accepted'),("Packed",'Packed'),("On The Way",'On The Way'),("Delivered",'Delivered'),("Cancel",'Cancel'))
	order_id = models.CharField(max_length=50,default='')
	seller = models.CharField(max_length=100,default='iheart@admin',)
	user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
	pins = models.CharField(max_length=50)
	# size = models.CharField(max_length=50,default='',null=True)
	status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='')