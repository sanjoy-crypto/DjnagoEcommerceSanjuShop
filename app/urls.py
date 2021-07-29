from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MypasswordResetForm, MySetPasswordForm
urlpatterns = [
    path('', views.home),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),

    path('buy/', views.buy_now, name='buy-now'),

    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),
    path('headphone/', views.headphone, name='headphone'),
    path('headphone/<slug:data>/', views.headphone, name='headphonedata'),
    path('television/', views.television, name='television'),
    path('television/<slug:data>/', views.television, name='televisiondata'),




    # path('login/', views.loginPage, name='login'),
    # path('logout/', views.logoutUser, name='logout'),
    path('registration/', views.customerregistration,
         name='customerregistration'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
         form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
         form_class=MypasswordResetForm), name="password_reset"),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'), name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'), name="password_reset_complete"),
]