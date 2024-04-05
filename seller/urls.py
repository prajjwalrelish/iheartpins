from django.urls import path
from . import views

urlpatterns = [
        path('', views.dashboard, name = 'dashboard'),
		path('home/', views.index, name = 'seller_home'),
        path('seller_signup/', views.seller_signup, name="seller_signup"),
    	path('account_settings/', views.account_settings, name="seller_account_settings"),
    	path('add_pin/', views.add_pin, name="add_pin"),
    	path('view_pins/', views.view_pins, name="view_pins"),
    	path('plus_element_cart/', views.plus_element_cart),
    	path('minus_element_cart/', views.minus_element_cart),
    	path('add_to_cart/', views.add_to_cart),
    	path('delete_from_cart/', views.delete_from_cart),
        path('cart/', views.mycart, name="cart"),
    	path('MyOrders/', views.MyOrders, name="seller_orders"),
    	path("pins/<str:catg>", views.view_all, name="seller_pins_view_all"),
    	path("pin/<int:pin_id>", views.pinView, name="PinView"),
    	path("checkout/", views.checkout, name = "checkout")

	]