"""Настраиваются URL проекта.

yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Дорогой Джанго, если на сервер пришёл любой запрос (''),
    # перейди в файл urls приложения posts
    # и проверь там все path() на совпадение с запрошенным URL
    # Добавляем к путям из приложения posts пространство имён posts (для ссылок)
    path("", include("posts.urls", namespace="posts")),
    # Если в приложении ice_cream не найдётся совпадений -
    # Django продолжит искать совпадения здесь, в головном файле urls.py.
    # Все адреса с префиксом auth/ в приложениие users
    path("auth/", include("users.urls", namespace="users")),
    # если не найдут будут прернаправлены в модуль django.contrib.auth
    path("auth/", include("django.contrib.auth.urls")),
    #  приложение about - статичные страницы
    path("about/", include("about.urls", namespace="about")),
    # для админки
    path("admin/", admin.site.urls),
]
