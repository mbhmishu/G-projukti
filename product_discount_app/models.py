from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
# from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('date', 'Date Wise'),
        ('time', 'Time Wise'),
    )
    AMOUNT_TYPE_CHOICES = (
        ('flat', 'Flat Amount'),
        ('percentage', 'Percentage Amount'),
    )
    
    type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    amount_type = models.CharField(max_length=10, choices=AMOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    def clean(self):
        if self.type == 'date':
            if not (self.start_date and self.end_date):
                raise ValidationError("For date-wise discount, start and end dates must be provided.")
            if self.start_date > self.end_date:
                raise ValidationError("Start date cannot be after end date.")
            if self.amount_type == 'percentage' and self.amount >= 100:
                raise ValidationError("Percentage amount must be less than 100.")
        elif self.type == 'time':
            if not (self.start_time and self.end_time):
                raise ValidationError("For time-wise discount, start and end times must be provided.")
            if self.start_time > self.end_time:
                raise ValidationError("Start time cannot be after end time.")
            if self.amount_type == 'percentage' and self.amount >= 100:
                raise ValidationError("Percentage amount must be less than 100.")
    
    def is_valid_discount(self):
        if self.type == 'date':
            now = timezone.now().date()
            return self.start_date <= now <= self.end_date
        elif self.type == 'time':
            now = timezone.now().time()
            return self.start_time <= now <= self.end_time
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.get_amount_type_display()}"
        


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    discount = models.ForeignKey('Discount', related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    
    def calculate_discount_amount(self):
        if self.discount:
            if self.discount.amount_type == 'percentage':
                return (self.price * self.discount.amount) / 100
            elif self.discount.amount_type == 'flat':
                return min(self.discount.amount, self.price)
        return Decimal('0.00')
    
    def actual_price(self):
        return self.price - self.calculate_discount_amount()
    
    def save(self, *args, **kwargs):
        # Round the price to 2 decimal places
        self.price = round(self.price, 2) 
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name



