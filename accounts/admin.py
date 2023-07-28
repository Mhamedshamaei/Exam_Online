from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import *
from .models import *


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ('email_phone', 'phone', 'email', 'national_code', 'role', 'is_active',)
    list_filter = ('is_active', 'role')
    fieldsets = (
        ('user', {'fields': ('email_phone', 'phone', 'email', 'national_code',)}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email_phone', 'phone', 'email', 'national_code', 'role', 'password1', 'password2')}),
    )
    search_fields = ('email_phone', 'phone', 'email', 'national_code', 'role',)
    ordering = ('phone', 'email', 'national_code', 'role')
    filter_horizontal = ()


class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'first_name', 'last_name', 'father_name', 'academy',)


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'first_name', 'last_name',)


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'first_name', 'last_name',)


class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'url',)


class AcademyGalleryAdmin(admin.ModelAdmin):
    list_display = ('alt', 'academy',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(OwnerProfile, OwnerProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(Academy, AcademyAdmin)
admin.site.register(AcademyGallery, AcademyGalleryAdmin)
admin.site.register(Courses)
admin.site.register(LoginImages)
admin.site.register(ActiveCode)
