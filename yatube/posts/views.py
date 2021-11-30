from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница')

# В урл мы ждем парметр, и нужно его прередать в функцию для использования


def group_posts(request, slug):
    return HttpResponse(f'Группа номер {slug}')
