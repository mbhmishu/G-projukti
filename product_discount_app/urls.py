from django.urls import path
from .views import (
    DiscountListCreateAPIView,
    DiscountDetailUpdateDeleteAPIView,
    ValidDiscountListAPIView,
    CategoryListAPIView,
    CategoryCreateAPIView,
    CategoryDetailUpdateDeleteAPIView,
    ProductListCreateAPIView,
    ProductDetailUpdateDeleteAPIView,
)

urlpatterns = [
    path('discounts/', DiscountListCreateAPIView.as_view(), name='discount-list-create'),
    path('discounts/<int:pk>/', DiscountDetailUpdateDeleteAPIView.as_view(), name='discount-detail-update-delete'),
    path('discounts/valid/', ValidDiscountListAPIView.as_view(), name='valid-discount-list'),
    path('create/categorie/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailUpdateDeleteAPIView.as_view(), name='category-detail-update-delete'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailUpdateDeleteAPIView.as_view(), name='product-detail-update-delete'),
]