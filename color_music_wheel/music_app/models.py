from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='app_users',
        related_query_name='app_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='app_users',
        related_query_name='app_user',
    )

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, default='#000000')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

class Features(models.Model):
    acousticness = models.FloatField(null=True)
    danceability = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    instrumentalness = models.FloatField(null=True)
    liveness = models.FloatField(null=True)
    loudness = models.FloatField(null=True)
    speechiness = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    valence = models.FloatField(null=True)

class Song(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # Using Spotify track ID as the primary key
    name = models.CharField(max_length=100, default='Unknown Song')
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    image = models.URLField(default='')
    features = models.OneToOneField(Features, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UserColorMusic(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    music = models.ManyToManyField(Song)

    def __str__(self):
        return f'{self.user.username} - {self.color.name}'

class MyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, default=1)  # Specify a default value here

    def __str__(self):
        return self.name
