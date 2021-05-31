from django.shortcuts import render
from django.views.generic.base import View

class Author(View):
    @staticmethod
    def get(request):
        return render(request, 'misc/author.html')


class Tech(View):
    @staticmethod
    def get(request):
        return render(request, 'misc/tech.html')
