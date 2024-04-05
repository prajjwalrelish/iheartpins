from django import template
from seller.models import Pin

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)


@register.filter(name='remfl')
def remfl(str1, key):
	if str1 != '' and key != '':
		return str(str1)[int(key):-int(key)]

@register.filter(name='pin')
def pin(str1, key):
	if str1.split(key)[0] != '':
		ppp = pin.objects.filter(pin_id=str1.split(key)[0]).first()
		return [ppp.pin_name,ppp.image1.url,ppp.price]
