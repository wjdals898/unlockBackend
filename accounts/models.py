from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, social_id=0, gender="F", password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            name=name,
            social_id=social_id,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        superuser = self.create_user(
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
    social_id = models.PositiveIntegerField(unique=True, null=True)
    email = models.EmailField(max_length=40, unique=True, null=False, blank=False)
    gender = models.CharField(max_length=10, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"({self.id}) {self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Counselor(models.Model):
    id = models.AutoField(primary_key=True)
    userkey = models.ForeignKey(User, on_delete=models.CASCADE,  db_column="userkey", related_name="counselor")


class Counselee(models.Model):
    id = models.AutoField(primary_key=True)
    userkey = models.ForeignKey(User, on_delete=models.CASCADE,  db_column="userkey", related_name="counselee")
