import re

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from unidecode import unidecode


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.PUBLISHED,
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок',
    )
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='Автор',
    )
    body = models.TextField(
        verbose_name='Контент',
    )
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name='Опубликовано',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено',
    )
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT,
        verbose_name='Статус',
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'
        ordering = (
            '-publish',
        )
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=(
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()

        super().save(*args, **kwargs)

    def generate_slug(self):
        value = self.title

        if not value:
            return ''
        slug = unidecode(value).lower()
        slug = re.sub(r'[^-\w]+', '-', slug).strip('-')

        # Ограничение длины, чтобы избежать слишком длинных слагов
        return slug[:50]


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Имя',
    )
    email = models.EmailField(
        verbose_name='E-mail',
    )
    body = models.TextField(
        verbose_name='Содержание',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Опубликован',
    )

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Комментарий от {self.name} на пост {self.post}'
