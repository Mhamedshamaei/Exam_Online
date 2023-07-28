from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import PasswordChangeForm
from six import text_type
from .forms import *
from academy.forms import *
import random
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash


def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner',login_url=login_url)


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_genetor = EmailToken()


def register(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = OwnerProfileForm(request.POST)
        academy_form = AcademyCreateForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and academy_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data
            academy_data = academy_form.cleaned_data
            user = User.objects.create_user(email=user_data['email'], phone=user_data['phone'],
                                            national_code=user_data['national_code'], password=user_data['password2'])
            user.email_phone = user.email
            user.role = 'Owner'
            user.save()
            academy = Academy.objects.create(name=academy_data['name'], url=academy_data['url'])
            academy.save()
            OwnerProfile.objects.create(first_name=profile_data['first_name'], last_name=profile_data['last_name'],
                                        father_name=profile_data['first_name'], owner=user, academy=academy)
            active_code = random.randint(111111, 999999)
            ActiveCode.objects.create(user=user, code=active_code)

            msg_html = render_to_string('accounts/email.html', {'code': active_code})

            send_mail(
                'فعال سازی حساب کاربری',
                'mahdihamedx@gmail.com',
                'active your account',
                [user.email],
                html_message=msg_html,
            )

            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes((user.id)))
            url = reverse('accounts:active', kwargs={'uidb64': uidb64, 'token': email_genetor.make_token(user)})
            link = 'http://' + domain + url
            messages.success(request, 'لطفا حساب کاربری خود را فعال کنید')
            return redirect(url)
        else:
            for error_user in user_form.errors:
                if error_user:
                    messages.error(request, error_user, 'danger')
            for error_academy in academy_form.errors:
                if error_academy:
                    messages.error(request, error_academy, 'danger')
    else:
        user_form = UserCreateForm()
        profile_form = OwnerProfileForm()
        academy_form = AcademyCreateForm()

    context = {'user_form': user_form, 'profile_form': profile_form, 'academy_form': academy_form}
    return render(request, 'accounts/register.html', context)


def resend(request, uidb64, token):
    id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=id)
    if user and email_genetor.check_token(user, token):
        active_code = ActiveCode.objects.filter(user_id=id)
        if active_code.exists():
            active_code.delete()
        active_code = random.randint(111111, 999999)
        ActiveCode.objects.create(user=user, code=active_code)
        msg_html = render_to_string('accounts/email.html', {'code': active_code})
        send_mail(
            'فعال سازی حساب کاربری',
            'mahdihamedx@gmail.com',
            'active your account',
            [user.email],
            html_message=msg_html,
        )
        data = {'success': 'ok'}
    else:
        return redirect('home:home')
    return JsonResponse(data)


def active(request, uidb64, token):
    id = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, id=id)
    if not user or not email_genetor.check_token(user, token):
        messages.error(request, 'مشکلی پیش آمده ، لطفا مجدد تلاش کنید')
        return redirect('accounts:login')

    if request.method == 'POST':
        form = ActiveCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['code']
            check = ActiveCode.objects.filter(user_id=user.id, code__exact=data)
            if check.exists():
                user.is_active = True
                user.save()
                check.delete()
                messages.success(request, 'حساب کاربری شما با موفقیت فعال شد')
                return redirect('accounts:login')
            else:
                messages.error(request, 'کد فعال سازی اشتباه است')
        else:
            messages.error(request, 'لطفا اطلاعات صحیح وارد کنید')
    else:
        form = ActiveCodeForm()
    context = {'user': user, 'uidb64': uidb64, 'token': token}
    return render(request, 'accounts/active.html', context)


def u_login(request):
    images = LoginImages.objects.all()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None and user.role == 'Owner':
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'کاربری با این مشخصات وجود ندارد')
        else:
            messages.error(request, 'لطفا اطلاعات صحیح وارد کنید')
    else:
        form = UserLoginForm()
    context = {'images': images}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def profile(request):
    if request.method == 'POST':
        profile_form = OwnerProfileForm(request.POST, request.FILES, instance=request.user.owner_profile)
        update_form = OwnerUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and update_form.is_valid():
            profile_form.save()
            update_form.save()
            messages.success(request, 'اطلاعات شما با موفقیت دخیره شد')
        else:
            messages.error(request, 'لطفا اطلاعات صحیح وارد کنید')
    else:
        profile_form = OwnerProfileForm(instance=request.user.owner_profile)
        update_form = OwnerUpdateForm(instance=request.user)
    context = {'profile_form': profile_form, 'update_form': update_form}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def u_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('accounts:login')
