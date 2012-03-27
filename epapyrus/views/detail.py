# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.db.models import get_model
from synergy.templates.regions.views import RegionViewMixin

class ArticleDetailView(RegionViewMixin ,DetailView,):
    model = get_model('epapyrus','Article')
    #template_name = 'epapyrus/article.html'
    
    def get_context_data(self, *args, **kwargs):    
        data = super(ArticleDetailView,self).get_context_data(*args, **kwargs)
        print data
        return data
        