from django.shortcuts import render


def index(request):
    template = 'posts/index.html'
    return render(request, template)
