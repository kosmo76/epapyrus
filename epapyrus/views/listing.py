# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import get_model

class ArticlesView(ListView):
    model = get_model('epapyrus','Article')
    template_name = 'epapyrus/articles.html'
    
    #queryset = get_model('osblog','Article').objects.filter(publish__exact=True);
    
class TagView(ListView):
    
    template_name = 'epapyrus/articles.html'
    
    def get_queryset(self):
        return get_model('epapyrus','PrimaryTagItem').objects.get_for_tag(self.kwargs['tag_code'])
      
    def get_context_data(self, *args, **kwargs):
        context = super(TagView, self).get_context_data(*args, **kwargs)
        for i in context['object_list']:
            print i
        
        return context 
        
class BookView(ListView):
    
    template_name = 'epapyrus/book.html'
    
    def get_queryset(self):
        return get_model('epapyrus','grouper').objects.filter(parent__exact=None)
      
    def get_context_data1(self, *args, **kwargs):
        context = super(TagView, self).get_context_data(*args, **kwargs)
        for i in context['object_list']:
            print i
        
        return context 
    