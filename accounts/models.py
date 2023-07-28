from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_delete


class UserManager(BaseUserManager):
    def create_user(self, email, phone, national_code, password):
        user = self.model(email_phone=self.normalize_email(email), email=self.normalize_email(email),
                          phone=phone, national_code=national_code)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, national_code, password, email_phone=None, ):
        user = self.create_user(email, phone, national_code, password)
        user.email_phone = user.email
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USER_ROLE = (
        ('Owner', 'owner'),
        ('Teacher', 'teacher'),
        ('Student', 'student'),
    )
    email_phone = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    national_code = models.IntegerField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices=USER_ROLE, max_length=100)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email_phone'
    REQUIRED_FIELDS = ('email', 'phone', 'national_code',)
    objects = UserManager()

    def __str__(self):
        return self.email_phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OwnerProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='owner_profile/', default='default_images/avatar.png')
    academy = models.OneToOneField('Academy', related_name='owner_academy', on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email_phone


class TeacherProfile(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    now_academy = models.ForeignKey('Academy', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.teacher.phone)


class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    now_academy = models.ForeignKey('Academy', on_delete=models.CASCADE, null=True, blank=True)
    now_courses = models.ManyToManyField('Courses')

    def __str__(self):
        return str(self.student.national_code)


class Academy(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='academy_images/', default='default_images/academy.png')
    url = models.CharField(max_length=100)
    courses = models.ManyToManyField('Courses', related_name='ac_courses')
    students = models.ManyToManyField(User, related_name='Academy_students')
    teachers = models.ManyToManyField(User, related_name='Academy_teachers')
    exam_num = models.PositiveIntegerField(default=3)

    def owner(self):
        data = OwnerProfile.objects.filter(academy_id=self.id)
        if data.exists():
            return data.get().owner.email_phone
        else:
            return None

    def __str__(self):
        return self.name


def delete_owner_academy(sender, instance, *args, **kwargs):
    data = instance
    academy = Academy.objects.filter(id=instance.academy.id)
    if academy.exists():
        academy.delete()


post_delete.connect(delete_owner_academy, sender=OwnerProfile)


class AcademyGallery(models.Model):
    alt = models.CharField(max_length=100, null=True, blank=True)
    g_image = models.ImageField(upload_to='academy_gallery/')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='gallery_academy')

    def __str__(self):
        return self.alt


class Courses(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name='Courses_students')
    teachers = models.ManyToManyField(User, related_name='Courses_teachers')
    create = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class ActiveCode(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, related_name='active_code_user', on_delete=models.CASCADE)
    code = models.PositiveIntegerField()

    def __str__(self):
        return self.user.email_phone


class LoginImages(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='login_images/')

    def __str__(self):
        return self.name
