from rest_framework import serializers
from .models import Discount,Category, Product

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        
    def validate(self, data):
        if data['type'] == 'date':
            if not (data.get('start_date') and data.get('end_date')):
                raise serializers.ValidationError("For date-wise discount, start and end dates must be provided.")
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date cannot be after end date.")
            if data['amount_type'] == 'percentage' and data['amount'] >= 100:
                raise serializers.ValidationError("Percentage amount must be less than 100.")
        elif data['type'] == 'time':
            if not (data.get('start_time') and data.get('end_time')):
                raise serializers.ValidationError("For time-wise discount, start and end times must be provided.")
            if data['start_time'] > data['end_time']:
                raise serializers.ValidationError("Start time cannot be after end time.")
            if data['amount_type'] == 'percentage' and data['amount'] >= 100:
                raise serializers.ValidationError("Percentage amount must be less than 100.")
        return data



class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('slug',)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_id = serializers.IntegerField(write_only=True, required=False)
    actual_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    calculate_discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category_name', 'price', 'discount_id','actual_price', 'calculate_discount_amount')
        read_only_fields = ('id',)

    def get_discount_info(self, instance):
        if instance.discount:
            return {
                'id': instance.discount.id,
                'type': instance.discount.get_type_display(),
                'amount_type': instance.discount.get_amount_type_display(),
                'amount': instance.discount.amount
            }
        return None

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', '')
        discount_id = validated_data.pop('discount_id', None)
        
        category, _ = Category.objects.get_or_create(name=category_name)
        discount = None
        
        if discount_id:
            discount = Discount.objects.filter(id=discount_id).first()
            if not discount:
                raise serializers.ValidationError(_("Invalid discount ID"))

        product = Product.objects.create(category=category, **validated_data, discount=discount)
        return product
    


class CategoryDetailsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'







