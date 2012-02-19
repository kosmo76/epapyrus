# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import get_model, Q

from synergy.templates.regions.views import RegionViewMixin

class ArticlesView(RegionViewMixin, ListView):
    model = get_model('epapyrus','Article')
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            q1 = Q(author__exact=self.request.user)
            q2 = Q(is_promoted__exact=True, is_published__exact=True)
            return get_model('epapyrus', 'Article').objects.filter(q1|q2)
        else:
            return get_model('epapyrus', 'Article').objects.filter(is_promoted__exact=True, is_published__exact=True);
    
    
    def get_context_data(self, *args, **kwargs):
        ctx = super(ArticlesView, self).get_context_data(*args, **kwargs)
        ctx['title'] = 'Promoted Articles'
        return ctx

class TagView(RegionViewMixin, ListView):
    
    def get_queryset(self):
        return get_model('epapyrus','PrimaryTagItem').objects.get_for_tag(self.kwargs['tag_code'])
      
    def get_context_data(self, *args, **kwargs):
        context = super(TagView, self).get_context_data(*args, **kwargs)
        return context 
        
class BookView(RegionViewMixin, ListView):
    def get_queryset(self):
        return get_model('epapyrus','grouper').objects.filter(parent__exact=None)
      
    def get_context_data(self, *args, **kwargs):
        context = super(BookView, self).get_context_data(*args, **kwargs)
        context['title'] = "Books"
        return context 
    
