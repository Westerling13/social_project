from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify
from markdown2 import markdown


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


class Story(models.Model):
    """Модель истории"""
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=100)
    # text = models.TextField('Текст')
    markdown_text = models.TextField('Markdown-текст', default='', help_text='Тест в формате Markdown')
    html_text = models.TextField('Обработанный текст', editable=False, default='')
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)
    edit_date = models.DateTimeField('Дата редактирования', auto_now=True)
    publication_date = models.DateTimeField('Дата публикации', default=timezone.now())
    published = models.BooleanField('Опубликована', default=True)
    url = models.SlugField('URL', default='', editable=False)

    def save(self, *args, **kwargs):
        url = self.title.lower()
        self.url = slugify(url)
        self.html_text = markdown(self.markdown_text)
        print(self.markdown_text)
        print(self.html_text)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('story', args=[self.url])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'
