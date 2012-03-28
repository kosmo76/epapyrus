# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.db.models import get_model
from synergy.templates.regions.views import RegionViewMixin

class ArticleDetailView(RegionViewMixin ,DetailView):
    model = get_model('epapyrus','Article')
    
    def get_context_data(self, *args, **kwargs):    
        data = super(ArticleDetailView,self).get_context_data(*args, **kwargs)
       
       #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        data['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return data
        
class ArticleDetailBookView(RegionViewMixin ,DetailView):
    model = get_model('epapyrus','Article')
    
    def get_context_data(self, *args, **kwargs):    
        data = super(ArticleDetailBookView,self).get_context_data(*args, **kwargs)
       
       #wywal TOC do sidebatu - powinno bc get_objcet_or_404
        data['toc'] = get_model('epapyrus','grouper').objects.get(pk__exact=self.kwargs['book_id'])
        data['region_postfixes'] = {'sidebar': 'book'}
        return data

class GrouperView(RegionViewMixin, DetailView):
    model = get_model('epapyrus','Grouper')
    
    def get_context_data(self, *args, **kwargs):    
        data = super(GrouperView,self).get_context_data(*args, **kwargs)
       
       #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        data['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return data
    