from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class Profile(models.Model):
    """Модель профиля пользователя"""
    GENDERS = [
        (None, 'Выберите пол'),
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    image = models.ImageField('Аватар', upload_to='users/', default='placeholder-200.png')
    gender = models.CharField('Пол', choices=GENDERS, blank=False, default=None, max_length=7, null=True)
    birth_date = models.DateField('Дата рождения', null=True, default=timezone.now)
    bio = models.TextField('Личная информация', max_length=1000)
    is_private = models.BooleanField('Приватный', default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user', args=[self.user.username])

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    """Сигнал на создание профиля пользователя при регистрации"""
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
