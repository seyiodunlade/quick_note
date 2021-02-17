from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django import forms
from django.utils import timezone


# Model Manager
class MyUserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, country, date_joined, password=None, **other_fields):

        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a Username')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        if not country:
            raise ValueError('Users must have a country specified')

        if not date_joined:

            raise ValueError('Users must have a date of signup specified')

        user = self.model(

            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            date_joined=date_joined

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, country, date_joined, password=None, **other_fields):

        user = self.create_user(email, username=username, password=password, first_name=first_name, last_name=last_name,
                                country=country, date_joined=date_joined, other_fields=other_fields)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)

        return user


# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(verbose_name="email_address", unique=True)
    date_joined = models.DateField()
    country = models.CharField(max_length=40)
    # secret_password = models.CharField(max_length=32, blank=True, widget=forms.PasswordInput)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'country', 'date_joined']

    def __str__(self):

        return self.username

    def get_full_name(self):

        return "%s %s" % (self.first_name, self.last_name)


class UserNotes(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    header = models.CharField(max_length=120)
    content = models.TextField()
    category = models.CharField(max_length=30)
    date_created = models.DateField(default=timezone.now())
    is_private = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    was_downloaded = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    last_edit = models.DateField('Last Edited date', default=timezone.now())


class Categories(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category1 = models.CharField(max_length=30, default="personal")
    category2 = models.CharField(max_length=30, default="work")
    category3 = models.CharField(max_length=30, default="education")
    category4 = models.CharField(max_length=30, default="others")
    category5 = models.CharField(max_length=30, blank=True)
    category6 = models.CharField(max_length=30, blank=True)
    category7 = models.CharField(max_length=30, blank=True)


class PublicNotes(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    note = models.ForeignKey(UserNotes, on_delete=models.CASCADE)
    note_link = models.URLField(unique=True, blank=True)
    shared_visits = models.IntegerField(default=0)


'''

    class Categories(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category1 = models.CharField(max_length="30")
    category2 = models.CharField(max_length="30")
    category3 = models.CharField(max_length="30")
    
    class MyNotes(models.Model):
        
        id
        user_id
        header
        content
        category
        date_created
        is_private
        shared
        shared_visits
        was_downloaded
        download_count
        
    class PrivateNotes(models.Model):
    
        id
        noteid
        
    
    users should be able to add their own categories
    
    work on pagination for notes
    
    work on downloadable notes
    work on shareable notes
    
'''