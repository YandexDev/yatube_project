"""Здесь можно настроить отображение админ-зоны приложения."""

from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    list_editable = ("group",)
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        "pk",
        "text",
        "pub_date",
        "author",
        "group",
    )
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # Добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    # Это свойство сработает для всех колонок: где пусто — там будет эта строка
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "description",
    )
    search_fields = ("text",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


# При регистрации модели Post источником конфигурации для неё назначаем
# класс PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
