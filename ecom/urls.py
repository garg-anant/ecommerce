from django.urls import path
from . import views

app_name='ecom'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('main', views.main, name='main'),
    # path('main_vendor', views.main_vendor, name='main_vendor')
    path('logout', views.logout_func, name='logout'),
    path('change_price/<int:ledger_id>', views.change_price, name='change_price')
]