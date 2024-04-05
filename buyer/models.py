from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserDetail(models.Model):
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
	dob = models.DateField(null = True)
	photo = models.ImageField(default='default.png',upload_to='user_photos')
	mobile = models.CharField(max_length=10,null=True)
	alternate_mobile = models.CharField(max_length=10,null=True,blank=True)
	address = models.TextField()
	pincode = models.CharField(max_length=6, null=True)
	landmark = models.CharField(max_length=500, null=True, blank=True)
	locality = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	sex = models.CharField(max_length=6,choices=SEX_CHOICES, null=True)
        
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.photo.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.photo.path)

class Slider(models.Model):
	name = models.CharField(max_length=50, default = "", null=True)
	image = models.ImageField(upload_to='slider_img')
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


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pin_id = models.CharField(max_length=100)
	pin_size = models.CharField(max_length=20,default='',null=True)
	number = models.PositiveIntegerField(default=0)

class Contact(models.Model):
	date = models.DateField(auto_now=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField()
	
	def __str__(self):
		return self.email