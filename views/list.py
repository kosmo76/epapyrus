# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import get_model

class ArticlesView(ListView):
    model = get_model('osblog','Article')
    template_name = 'osblog/articles.html'