from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:product_slug>/', views.product_infor, name='product-infor'),
    path('search/<slug:category_slug>/', views.list_category, name='list-category')
]
