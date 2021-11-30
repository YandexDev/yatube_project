# ice_cream/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
    # Страницы сообществ ждем переменную slug типа slug
    # Конвертор тип slug - строки и положиетельные числа
    # path('group/<slug:slug>/', views.group_posts), Пока не создана функция group_posts
]
