from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import safe
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from pytils.translit import slugify
from markdown2 import markdown


class Profile(models.Model):
    """Модель профиля пользователя"""
    GENDERS = [
        ('Не указан', 'Не указан'),
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Электронный адрес', max_length=50)
    image = models.ImageField('Аватар', upload_to='users/', default='placeholder-200.png')
    gender = models.CharField('Пол', choices=GENDERS, blank=False, default='Не указан', max_length=9, null=True)
    birth_date = models.DateField('Дата рождения', null=True, default=timezone.now)
    bio = models.TextField('Личная информация', max_length=1000, blank=True, default='')
    is_private = models.BooleanField('Приватный', default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user', args=[self.user.username])

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['pk']


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
    as_md = models.BooleanField('Использовать Markdown', default=False)
    text = models.TextField('Текст', default='')
    html_text = models.TextField('Обработанный текст', editable=False, default='')
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)
    edit_date = models.DateTimeField('Дата редактирования', auto_now=True)
    publication_date = models.DateTimeField('Дата публикации', default=timezone.now)
    published = models.BooleanField('Опубликована', default=True)
    slug = models.SlugField('slug', default='', editable=False)

    def save(self, *args, **kwargs):
        slug = self.title.lower()
        self.slug = slugify(slug)
        if self.as_md:
            self.html_text = markdown(self.text)
        else:
            self.html_text = self.text
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('story', args=[self.pk, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'
        ordering = ['-publication_date']


class Comment(models.Model):
    """Модель комментария"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name='История')
    text = models.TextField('Текст')
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.author} -> {self.story}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-creation_date']
