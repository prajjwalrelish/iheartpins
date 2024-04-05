from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from seller.views import admin2

urlpatterns = [
    path('buyer/india/my/admin/pannel/home/', admin.site.urls),
    path('buyer/india/my/admin/pannel/admin20/', admin2, name = 'admin2'),
    path('', include('buyer.urls')),
    path('seller/', include('seller.urls')),
    path("login/", auth_views.LoginView.as_view(template_name='buyer/login.html', redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='buyer/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='buyer/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='buyer/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='buyer/password_reset_complete.html'), name="password_reset_complete"),
    path("coupon/",include('coupon.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
