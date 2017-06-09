from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField

# Member must be in the __init__.py file so django can import it directly from the models module


class MemberManager(BaseUserManager):
    def create_member(self, email, rfid, first_name, last_name, phone_number, password=None):
        """
        Creates and saves a Member with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        member = self.model(
            email=self.normalize_email(email),
            rfid=rfid,
            first_name=first_name,
            last_name=last_name,
            date_joined=now(),
            phone_number=phone_number
        )

        member.set_password(password)
        member.save(using=self._db)
        return member

    def create_superuser(self, email, rfid, first_name, last_name, phone_number, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        superuser = self.create_member(
            email=email,
            rfid=rfid,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser


class Member(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    rfid = models.CharField(
        verbose_name="RFID",
        max_length=10,
        unique="True"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(unique=True)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rfid', 'first_name', 'last_name', 'phone_number']

    def get_full_name(self):
        # The user is identified by their email address
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin