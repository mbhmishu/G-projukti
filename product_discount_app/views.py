from rest_framework import generics
from rest_framework.response import Response
from .models import Discount,Category, Product
from .serializers import DiscountSerializer,CategoryListSerializer, ProductSerializer,CategoryCreateSerializer,CategoryDetailsSerializer
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions
from rest_framework import serializers






class DiscountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    # permission_classes = (permissions.IsAuthenticated, (if needed)Custom permissions,)




class DiscountDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer




class ValidDiscountListAPIView(generics.ListAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        now = timezone.now()
        return Discount.objects.filter(
            Q(type='date', start_date__lte=now, end_date__gte=now) |
            Q(type='time', start_time__lte=now.time(), end_time__gte=now.time())
        )




class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer




class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer




class CategoryDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().prefetch_related('products__discount')
    serializer_class = CategoryDetailsSerializer
   



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().select_related('category', 'discount')
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        category_name = self.request.data.get('category_name')
        discount_id = self.request.data.get('discount_id')
        
        category, _ = Category.objects.get_or_create(name=category_name)
        discount = None
        
        if discount_id:
            discount = Discount.objects.filter(id=discount_id).first()
            if not discount:
                raise serializers.ValidationError(_("Invalid discount ID"))

        serializer.save(category_name=category_name, discount_id=discount_id)




class ProductDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related('category', 'discount')
    serializer_class = ProductSerializer
  
