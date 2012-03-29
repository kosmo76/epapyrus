# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import get_model, Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from synergy.templates.regions.views import RegionViewMixin



class ArticlesView(RegionViewMixin,ListView ):
    model = get_model('epapyrus','Article')
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            q1 = Q(author__exact=self.request.user)
            q2 = Q(is_promoted__exact=True, is_published__exact=True)
            return get_model('epapyrus', 'Article').objects.filter(q1|q2)
        else:
            return get_model('epapyrus', 'Article').objects.filter(is_promoted__exact=True, is_published__exact=True);
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesView, self).get_context_data(*args, **kwargs)
        
        #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        
        return context

class TagView(RegionViewMixin, ListView):
    
    def get_queryset(self):
        #tylko dla artykulow
        return get_model('epapyrus','PrimaryTagItem').objects.get_for_tag(self.kwargs['tag_code'])
      
    def get_context_data(self, *args, **kwargs):
        context = super(TagView, self).get_context_data(*args, **kwargs)
        #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return context 
        
class BooksView(RegionViewMixin, ListView):
    def get_queryset(self):
        return get_model('epapyrus','grouper').objects.filter(parent__exact=None)
      
    def get_context_data(self, *args, **kwargs):
        context = super(BooksView, self).get_context_data(*args, **kwargs)
        #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return context 
 
class ShowNotes(RegionViewMixin,ListView):
    
     
    def _get_content_objects(self, model_name, obj_id):
        content_type = ContentType.objects.get(app_label="epapyrus", model=model_name)
        return get_model('epapyrus','Note').objects.filter(content_type__exact=content_type, object_id__exact=obj_id)
        
        
    def get_queryset(self):
        return self._get_content_objects(self.kwargs['model_name'], self.kwargs['obj_id'])
        
      
    def get_context_data(self, *args, **kwargs):
        context = super(ShowNotes, self).get_context_data(*args, **kwargs)
        
        
        parent_model  = ContentType.objects.get(app_label="epapyrus", model=self.kwargs['model_name'])
        context['parent'] = parent_model.model_class().objects.get(id__exact=self.kwargs['obj_id'])
        context['parent_type'] = parent_model
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        
        return context 
    
