from django.views.generic.base import View, TemplateView
from django.shortcuts import render


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class CocTV(TemplateView):
    template_name = 'coc.html'
