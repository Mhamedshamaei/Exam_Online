from django.db import models
from accounts.models import User


class Plans(models.Model):
    name = models.CharField(max_length=100)
    d_1 = models.CharField(max_length=100)
    d_2 = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to='plans_image/')
    exam_num = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CharField)
    plan = models.OneToOneField(Plans, on_delete=models.CASCADE,null=True)
    create = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    coupon = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.user.email

    def get_price(self):
        total = self.price
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    discount = models.IntegerField()

    def __str__(self):
        return self.code

class PayHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    create = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plans,on_delete=models.CASCADE,null=True)
    coupon = models.PositiveIntegerField(null=True,blank=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.user.email_phone
