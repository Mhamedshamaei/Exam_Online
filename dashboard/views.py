from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required


def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner', login_url=login_url)


@login_required(login_url='accounts:login')
@owner_required()
def home(request):
    return render(request, 'dashboard/home.html')
