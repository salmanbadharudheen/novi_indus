

from django.urls import path
from . import views

app_name = 'cartapp'

urlpatterns = [
    path('allprodcat/', views.allprodcat, name='allprodcat'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('delete/<int:product_id>/', views.cart_delete, name='cart_delete'),
    path('<slug:c_slug>/<slug:product_slug>/', views.proDetail, name='prodcatdetail'),
    path('<slug:c_slug>/', views.allprodcat, name='products_by_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]
