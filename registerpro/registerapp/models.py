from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class PhoneNumber(models.Model):
    phone=models.CharField(max_length=12,null=True,blank=True)

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True,blank=True)
    gender_type=(
        ('Male','Male'),
        ('Female','Female'),
    )
    gender=models.CharField(choices=gender_type,max_length=6)
    role_type=(
        ('Company','Company'),
        ('Agent','Agent'),
        ('Welder','Welder'),
    )
    role=models.CharField(choices=role_type,max_length=7)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    mobile=models.ManyToManyField(PhoneNumber)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Job(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='job')
    title=models.CharField(max_length=255,null=True,blank=True)
    description=models.CharField(max_length=255,null=True,blank=True)
    salary=models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.user.first_name 