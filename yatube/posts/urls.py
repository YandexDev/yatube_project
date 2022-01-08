"""Функция path(). Она принимает обязательные параметры path('route', view):
route — шаблон обрабатываемого адреса, образец, с которым сравнивается полученный запрос;
view — функция-обработчик: если запрошенный URL совпадает с route,
вызов будет перенаправлен в указанную view-функцию
(view-функции в Django хранят в файле views.py)."""

from django.urls import path

from . import views

# Эта строчка обязательна.
# Без неё namespace работать не будет:
# namespace должен быть объявлен при include и тут, в app_name
app_name = "posts"

urlpatterns = [
    path("", views.index, name="index"),
    # slug перед переменной - слова и цифры
    path("group/<slug:slug>/", views.group_posts, name="group_list"),
    # Профайл пользователя
    path("profile/<str:username>/", views.profile, name="profile"),
    # Просмотр записи
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    # Создание нового поста
    path("create/", views.post_create, name="post_create"),
    # Редактирование поста
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
]
