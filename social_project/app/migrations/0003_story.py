# Generated by Django 3.0.3 on 2020-02-09 16:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20200209_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('publication_date', models.DateTimeField(default=datetime.datetime(2020, 2, 9, 16, 14, 48, 171702, tzinfo=utc), verbose_name='Дата публикации')),
                ('published', models.BooleanField(default=True, verbose_name='Опубликована')),
                ('url', models.SlugField(default='', editable=False, verbose_name='URL')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'История',
                'verbose_name_plural': 'Истории',
            },
        ),
    ]
