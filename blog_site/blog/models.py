import re

from django.conf import settings
from django.db import models
from django.utils import timezone
from unidecode import unidecode


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
        unique=True,
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
