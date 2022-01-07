"""Тут хранятся обработчики запросов 
(функции или классы, получающие запрос и генерирующие ответ).
на вход объект запроса HttpRequest
на выходе объект ответа HttpResponse

from django.http import HttpResponse
# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из urls.py - path('ice_cream/<int:pk>/', views.ice_cream_detail):

def icecream_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')

Функция render() не только связывает view-функцию и шаблон, но и позволяет
передать в этот шаблон данные, сгенерированные во view-функции.
Данные, предназначенные для вывода на страницу, упаковывают в словарь
и передают в функцию render() в качестве третьего, необязательного аргумента.
Ключи словаря в специальных тегах подставляют в шаблон — и при рендеринге 
вместо этих ключей будут выведены значения, связанные с этими ключами.
"""

from django.contrib.auth.decorators import login_required

# render() возвращает шаблоны из файла
from django.shortcuts import get_object_or_404, render

from .models import Group, Post


def index(request):
    # в переменную posts будет сохранена выборка из 10 объектов модели Post
    # по специальной точки входа .objects,
    # отсортированных по полю pub_date по убыванию (в мета-классе модели)
    posts = Post.objects.all()[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        "posts": posts,
    }
    # Полученные записи передаются в код как объекты класса Post,
    # сохраняются в виде списка в переменной posts и передаются в словаре context
    # под ключом 'posts' в шаблон posts/index.html.

    template = "posts/index.html"
    # TODO: Узнать больше про функцию render
    return render(request, template, context)


# View-функция для страницы сообщества:
@login_required  # Декторатор. Функция будет работать только авторизованным
def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    # posts = Post.objects.filter(group=group).order_by('-pub_date')[:10] ниже одинакого
    #  group.groups — это выборка тех объектов из модели Post,
    #  у которых в поле slug стоит "slug" (которые связаны с group),
    #  потому что group — это объект Group с slug=slug (который в url)
    posts = group.groups.all()[:10]

    context = {
        "group": group,
        "posts": posts,
    }

    template = "posts/group_list.html"

    return render(request, template, context)
