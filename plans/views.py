from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.contrib import messages
from .models import *
from .forms import *
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from accounts.models import Academy


def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner', login_url=login_url)


@login_required(login_url='accounts:login')
@owner_required()
def plans(request):
    plans = Plans.objects.all()
    context = {'plans': plans}
    return render(request, 'plans/plans.html', context)


def by_plans(request, id):
    plan = get_object_or_404(Plans, id=id)
    same_order = Order.objects.filter(user=request.user)
    if same_order.exists():
        same_order.delete()
    order = Order.objects.create(user=request.user, price=plan.price.replace(',', ''), plan=plan)
    return redirect('plans:order', order.id)


def order(request, id):
    order = get_object_or_404(Order, id=id)
    if order.user != request.user:
        return HttpResponseNotFound()
    plan = order.plan
    coupon = order.coupon
    context = {'order': order, 'plan': plan, 'coupon': coupon}
    return render(request, 'plans/details.html', context)


def coupon(request, id):
    order = get_object_or_404(Order, id=id)
    if order.user != request.user:
        return HttpResponseNotFound()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['code']
            time = timezone.now()
            try:
                coupon = Coupon.objects.get(code__iexact=data, active=True, start__lte=time, end__gte=time)
            except Coupon.DoesNotExist:
                messages.warning(request, 'کد تخفیف یافت نشد')
                return redirect('plans:order', order.id)
            order.discount = coupon.discount
            order.coupon = coupon.discount
            order.save()
            messages.success(request, 'کد تخفیف اعمال شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect('plans:order', order.id)


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/order:verify/'


def send_request(request, price, order_id):
    global amount
    amount = price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    # authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
        academy.exam_num += order.plan.exam_num
        academy.save()
        PayHistory.objects.create(price=order.price,plan=order.plan,coupon=order.coupon,user=request.user)

        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


@login_required(login_url='accounts:login')
@owner_required()
def pay_history(request):
    history = PayHistory.objects.filter(user=request.user).order_by('-create')
    total_exam = request.user.owner_profile.academy.exam_num
    context = {'history':history,'total_exam':total_exam}
    return render(request, 'plans/pay.html',context)
