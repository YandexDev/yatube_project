"""Тут хранятся обработчики запросов 
(функции или классы, получающие запрос и генерирующие ответ).
на вход объект запроса HttpRequest
на выходе объект ответа HttpResponse

from django.http import HttpResponse
Страница с информацией об одном сорте мороженого(как пример);
view-функция принимает параметр pk из urls.py - path('ice_cream/<int:pk>/', views.ice_cream_detail):

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
from django.core.paginator import Paginator

# render() возвращает шаблоны из файла
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    # в переменную posts будет сохранена выборка из 10 объектов модели Post
    # по специальной точки входа .objects,
    # отсортированных по полю pub_date по убыванию (в мета-классе модели)
    posts = Post.objects.all()
    # Показывать по 10 записей на странице
    paginator = Paginator(posts, 10)
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get("page")
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # В словаре context отправляем информацию в шаблон
    context = {
        "page_obj": page_obj,
    }
    # Полученные записи передаются в код как объекты класса Post,
    # сохраняются в виде списка в переменной page_obj и передаются в словаре context
    # под ключом 'page_obj' в шаблон posts/index.html.

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
    posts = group.groups.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
    }

    template = "posts/group_list.html"

    return render(request, template, context)


# Создание страницы профайла
def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    count = author.posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "count": count,
        "author": author,
    }

    template = "posts/profile.html"

    return render(request, template, context)


# Создание страницы отдельного поста
def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    pub_date = post.pub_date
    post_title = post.text[:30]
    author = post.author
    author_posts = author.posts.all().count()
    context = {
        "post": post,
        "post_title": post_title,
        "author": author,
        "author_posts": author_posts,
        "pub_date": pub_date,
    }

    template = "posts/post_detail.html"

    return render(request, template, context)


# Для создания нового поста
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(f"/profile/{post.author}/", {"form": form})
    form = PostForm()
    groups = Group.objects.all()
    template = "posts/create_post.html"
    context = {"form": form, "groups": groups}
    return render(request, template, context)


# Редактирование поста
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    groups = Group.objects.all()
    form = PostForm(request.POST or None, instance=post)
    template = "posts/create_post.html"
    if request.user == author:
        if request.method == "POST" and form.is_valid:
            post = form.save()
            return redirect("posts:post_detail", post_id)
        context = {
            "form": form,
            "is_edit": is_edit,
            "post": post,
            "groups": groups,
        }
        return render(request, template, context)
    return redirect("posts:post_detail", post_id)
