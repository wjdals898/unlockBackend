from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_social_user(self, email, password, social_id, name, gender="F"):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            social_id=social_id,
            name=name,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_normal_user(self, email, password, name, gender, birth):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            name=name,
            gender=gender,
            birth=birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, name, gender, birth):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            name=name,
            gender=gender,
            birth=birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        superuser = self.create_normal_user(
            email=email,
            password=password,
            name=email,
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    social_id = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=40, unique=True, null=False, blank=False)
    gender = models.CharField(max_length=10, null=True)
    birth = models.DateField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"({self.id}) {self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return f'/account/'


class CounselingType(models.Model):
    type = models.CharField(max_length = 30)


class Counselor(models.Model):
    id = models.AutoField(primary_key=True)
    userkey = models.ForeignKey(User, on_delete=models.CASCADE,  db_column="userkey", related_name="counselor_id")
    institution_name = models.CharField(max_length=50)
    institution_address = models.CharField(max_length=100)
    credit = models.CharField(max_length=30)
    prof_field = models.ForeignKey(CounselingType, on_delete=models.CASCADE, db_column='prof_field')


class Counselee(models.Model):
    id = models.AutoField(primary_key=True)
    userkey = models.ForeignKey(User, on_delete=models.CASCADE,  db_column="userkey", related_name="counselee_id")
