"""Здесь описывается устройство базы данных приложения.
Свойства модели, описанные через синтаксис имя_свойства = models.тип_данных(),
определят названия и типы данных в колонках таблицы БД.

Для создания поля со ссылкой на модель User импортируется и эта модель:
она встроена в Django и отвечает за управление пользователями.

ForeignKey - поле, в котором указывается ссылка на другую модель, или, в терминологии баз данных,
ссылка на другую таблицу, на её primary key (pk).
Это свойство обеспечивает связь (relation) между таблицами баз данных.
"""

from django.contrib.auth import get_user_model
from django.db import models

# Официальная документация рекомендует обращаться к модели User через функцию get_user_model
User = get_user_model()

# Объявляем класс Group, наследник класса Model из пакета models
class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    # параметр auto_now_add определяет, что в поле будет автоматически
    # подставлено время и дата создания новой записи
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        # Если из таблицы User будет удалён пользователь, то будут удалены все связанные с ним посты
        on_delete=models.CASCADE,
        # TODO: Почитать больше про related_name
        # У модели User автоматически появится свойство posts, оно ссылается на все записи текущего автора.
        related_name="posts",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="groups",
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
