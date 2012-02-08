# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.db.models import get_model

class ArticleDetailView(DetailView):
    model = get_model('epapyrus','Article')
    template_name = 'epapyrus/article.html'
    

        