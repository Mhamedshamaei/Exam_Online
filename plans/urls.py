from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('', views.plans, name='plans'),
    path('<int:id>/',views.by_plans,name='by_plans'),
    path('order/<int:id>/', views.order, name='order'),
    path('coupon/<int:id>/',views.coupon,name='coupon'),
    path('request/<int:order_id>/<int:price>/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('pay_history/', views.pay_history, name='pay_history')
]
