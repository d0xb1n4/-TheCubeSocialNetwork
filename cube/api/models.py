import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class CustomUser(AbstractUser, PermissionsMixin):
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='ава'
    )

    nickname = models.CharField(
        max_length=9,
        blank=False,
        verbose_name='никнейм'
    )
    token = models.TextField(
        blank=False,
        verbose_name='токен авторизации'
    )
    date_of_birth = models.DateField(
        blank=False,
        verbose_name='дата рождения'
    )
    date_of_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата регистрации'
    )
    status_emoji = models.TextField(
        blank=True,
        verbose_name='эмодзи статуса',
        default='❓'
    )
    status = models.TextField(
        blank=True,
        default='Нажмите для редактирования',
        verbose_name='статус'
    )
    subscribers = models.ManyToManyField(
        'CustomUser',
        blank=True,
        related_name='Подписчики')
    subscriptions = models.ManyToManyField(
        'CustomUser',
        blank=True,
        related_name='Подписки')

    # настройки приватности
    show_posts = models.BooleanField(
        default=True
    )
    show_status = models.BooleanField(
        default=True
    )
    show_sub_info = models.BooleanField(
        default=True
    )
    show_subscribers = models.BooleanField(
        default=True
    )
    show_subscriptions = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @staticmethod
    def generate_token(username):
        return \
            username + ''.join(
                [random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(15)]
            )

    def __str__(self):
        return self.nickname


class Post(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='+', on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser, related_name='+')
    image = models.ImageField(upload_to='posts/images/')
    document = models.FileField(upload_to='posts/docs/')
    music = models.FileField(upload_to='posts/music/')
    theme = models.CharField(max_length=20)
    text = models.TextField()

    closed_comments = models.BooleanField(default=False)

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, related_name='+', on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser, related_name='+')
    text = models.TextField()

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
