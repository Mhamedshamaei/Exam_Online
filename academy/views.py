from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q



def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner', login_url=login_url)


@login_required(login_url='accounts:login')
@owner_required()
def academy(request):
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    images = AcademyGallery.objects.filter(academy_id=academy.id)
    if request.method == 'POST':
        form = AcademyUpdateForm(request.POST, request.FILES, instance=academy)
        if form.is_valid():
            data = form.cleaned_data
            if Academy.objects.filter(~Q(id=academy.id), url__exact=data['url']).exists():
                messages.warning(request, 'آدرس مورد نظر موجود است')
                return redirect(request.META.get('HTTP_REFERER'))
            form.save()
            academy.url = academy.url.replace(" ", '-')
            academy.save()
            messages.success(request, 'با موفقیت ذخیره شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
            print(form.errors)
    else:
        form = AcademyUpdateForm(instance=academy)
    context = {'academy': academy, 'images': images, 'form': form}
    return render(request, 'academy/academy.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def add_img(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        images = AcademyGallery.objects.filter(academy_id=request.user.owner_profile.academy.id)
        if images.count() >= 3:
            messages.warning(request, 'حداکثر میتوانید 3 بنر داشته باشید')
        else:
            form = AcademyImageForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data['g_image']
                AcademyGallery.objects.create(g_image=data, alt=f'banner {images.count() + 1}',
                                              academy=request.user.owner_profile.academy)
                messages.success(request, 'عکس مورد نظر اضافه شد')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def delete_img(request, id):
    url = request.META.get('HTTP_REFERER')
    image = get_object_or_404(AcademyGallery, academy_id=request.user.owner_profile.academy.id, id=id)
    if image is not None:
        image.delete()
        messages.success(request, 'با موفقیت حذف شد')
    return redirect(url)
