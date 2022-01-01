"""Настройка конфигурации приложения"""

from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = "posts"
    # Тут можно указать, например, поле verbose_name
    # под этим именем приложение будет видно в админке.
    verbose_name = "Управление постами"
