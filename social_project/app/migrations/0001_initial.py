# Generated by Django 3.0.3 on 2020-02-10 16:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('as_md', models.BooleanField(default=False, verbose_name='Использовать Markdown')),
                ('text', models.TextField(default='', verbose_name='Текст')),
                ('html_text', models.TextField(default='', editable=False, verbose_name='Обработанный текст')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('publication_date', models.DateTimeField(default=datetime.datetime(2020, 2, 10, 16, 46, 4, 75844, tzinfo=utc), verbose_name='Дата публикации')),
                ('published', models.BooleanField(default=True, verbose_name='Опубликована')),
                ('url', models.SlugField(default='', editable=False, verbose_name='URL')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=50, verbose_name='Электронный адрес')),
                ('image', models.ImageField(default='placeholder-200.png', upload_to='users/', verbose_name='Аватар')),
                ('gender', models.CharField(choices=[('Не указан', 'Выберите пол'), ('Мужской', 'Мужской'), ('Женский', 'Женский')], default=('Не указан', 'Выберите пол'), max_length=9, null=True, verbose_name='Пол')),
                ('birth_date', models.DateField(default=django.utils.timezone.now, null=True, verbose_name='Дата рождения')),
                ('bio', models.TextField(blank=True, max_length=1000, verbose_name='Личная информация')),
                ('is_private', models.BooleanField(default=False, verbose_name='Приватный')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
