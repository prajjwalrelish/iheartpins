from django.contrib import admin
from .models import UserDetail, Slider, Contact, Cart
from seller.models import SellerSlider
from seller.models import Pin, PinSize, SellerInfo, category, dow, MyCart, PinSet, Orders, trend, PinSetOrders

admin.site.site_header = 'buyer'

admin.site.register(UserDetail)
admin.site.register(Pin)
admin.site.register(PinSize)
admin.site.register(SellerInfo)
admin.site.register(Slider)
admin.site.register(category)
admin.site.register(dow)
admin.site.register(Contact)
admin.site.register(SellerSlider)
admin.site.register(MyCart)
admin.site.register(PinSet)
admin.site.register(PinSetOrders)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(trend)