__author__ = 'rrmerugu'
from django.db import models
import logging
from django.utils import  timezone
logger = logging.getLogger(__name__)
from django.db.models import permalink
from django.utils.text import slugify
from .utils import get_object_or_none
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from random import randint

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver



class CustomUserQuerySet(models.QuerySet):
    def active_users(self, *args, **kwargs):
        return self.filter( is_active =True ,*args, **kwargs).order_by('-date_joined')


class CustomUserManager(BaseUserManager):

    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def active_users(self):
        return self.get_queryset().active_users()

    def create_user(self, email, first_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            is_staff=False,
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password):
        user = self.create_user(email,
                first_name=first_name,
                password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def register_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)

        ## gather the token for the user and return it
        return user


from django.core import serializers

class MyUser(AbstractBaseUser):
    salutation_choices = (
        ('mr','Mr.'),
        ('mrs', 'Mrs'),
        ('dr', 'Dr'),
        ('prof', 'Prof'),
        ('sir', 'Sir')
    )
    # Last login, is active, and password are included automatically
    user_id = models.AutoField(primary_key=True)
    username =  models.CharField(max_length=30, blank=True, null=True)
    email    =  models.EmailField(max_length=150, blank=False, primary_key=False,  unique=True)
    date_joined =  models.DateTimeField(auto_now_add=True, null=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="name")
    tag_line = models.CharField(max_length=100, null=True, verbose_name="Professional Heading")
    salutation = models.CharField(max_length=100, choices = salutation_choices, blank=True, null=True)
    profile_pic = models.FileField(upload_to='user-profile-pic', default="images/placeholders/user-placeholder.png")

    website = models.CharField(max_length=60, null=True, blank=True, )
    location = models.CharField(max_length=60, null=True, )
    biodata = models.TextField(max_length=2000, null=True, blank=True,verbose_name="About Me")

    # contributions = models.ForeignKey(Contribution)
    fb_link = models.CharField(max_length=100, blank=True, null=True)
    tw_link = models.CharField(max_length=100, blank=True, null=True)
    ln_link = models.CharField(max_length=100, blank=True, null=True)
    gh_link = models.CharField(max_length=100, blank=True, null=True)

    # Permission | Administration Purpose
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


 


    ## define the user manager class for User
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',]


    def __str__(self): # __unicode__ on Python 2
        return self.email
    # These are needed for the admin
    # https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#custom-users-and-django-contrib-admin
    # Full example - https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#a-full-example
    def get_tag_line(self):
        return self.tag_line or ''

    def get_full_name(self):
        return "%s %s".rstrip() %(self.first_name, self.last_name or '')

    def get_short_name(self):
        return "%s" %self.first_name

    def get_basic_info(self):
        data ={}
        data['profile_pic'] = self.profile_pic
        data['user_id'] = self.user_id
        data['username'] = self.username
        data['full_name'] = self.get_full_name()
        return data

    def generate_username(self):
        username = slugify(self.email.rstrip().split("@")[0])
        if get_object_or_none('MyUser', username=username):
            logger.debug(username)
            return "%s-%s"%(username,randint(1,99))
        else:
            return username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    class Meta:
        app_label = "core"

    @permalink
    def get_absolute_url(self):
        return ('view_user', None, { 'slug': self.user_id })



    def save(self, *args, **kwargs):
        logger.debug("user save triggered")
        self.full_name = self.get_full_name()
        self.username = self.generate_username()
        super(MyUser, self).save(*args, **kwargs)
