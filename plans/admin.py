from django.contrib import admin
from .models import *


class PlansAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'exam_num',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'create', 'price', 'discount', 'paid',)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'start', 'end', 'discount', 'active',)


admin.site.register(Plans, PlansAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(PayHistory)
