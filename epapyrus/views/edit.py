# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import get_model
from epapyrus.forms import forms

from django.db.models.signals import post_save
from django.dispatch import receiver
import django.dispatch

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404  
from django.core.urlresolvers import reverse

from synergy.templates.regions.views import RegionViewMixin

tag_save = django.dispatch.Signal(providing_args=['parent','tag'])
obj_delete = django.dispatch.Signal(providing_args=['obj'])


class ArticleImageCreateView(RegionViewMixin, CreateView):
    model = get_model('epapyrus', 'ArticleImage')
    template_name = 'epapyrus/image_add.html'
    form_class = forms.AddImage
 

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = get_model('epapyrus','article').objects.get(pk=self.kwargs['article'])
        self.object.save()
        
        return HttpResponseRedirect("/article/%s/edit/"% self.kwargs['article'])

class ArticleCreateView(RegionViewMixin, CreateView):
    model = get_model('epapyrus', 'Article')
    form_class = forms.CreateArticle

    #to powinno byc w inicie, ale nie moge zwalczyc gdzie jest tworzone form
    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['form'].fields['teaser'].widget.attrs['class'] = 'teaser'
        #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author=self.request.user;
        self.object.save()
        tag_save.send(sender=ArticleCreateView,  parent = self.object, tag=form.cleaned_data.get('tag'))
        return HttpResponseRedirect("/article/%s/" % self.object.id)
        
class GrouperCreateView(RegionViewMixin, CreateView):
    model = get_model('epapyrus','Grouper')
    
    form_class = forms.CreateGrouper
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author=self.request.user;
        self.object.save()
        #tag_save.send(sender=ArticleCreateView,  parent = self.object, tag=form.cleaned_data.get('tag'))
        return HttpResponseRedirect('/')
    
    
    
class ArticleUpdateView(RegionViewMixin, UpdateView):
    model = get_model('epapyrus', 'Article')
    form_class = forms.CreateArticle
    
        
    def get_initial(self):
        super(ArticleUpdateView, self).get_initial()
    
        if self.object.author != self.request.user:
            raise Http404
      
        self.initial['tag']=self.object.get_tag().values_list('id',flat=True)
    
        return self.initial
        
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.author=self.request.user;
        self.object.save()
        tag_save.send(sender=ArticleCreateView,  parent = self.object, tag=form.cleaned_data.get('tag'))
        return HttpResponseRedirect("/article/%s/" % self.object.id)    

     #to powinno byc w inicie, ale nie moge zwalczyc gdzie jest tworzone 
    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['teaser'].widget.attrs['class'] = 'teaser'
        context['images'] =  self.object.article_images.all()
         #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return context


class GrouperUpdateView(RegionViewMixin, UpdateView):
    model = get_model('epapyrus', 'Grouper')
    form_class = forms.CreateGrouper
    
        
    def get_initial(self):
        super(GrouperUpdateView, self).get_initial()
    
        if self.object.author != self.request.user:
            raise Http404
      
        self.initial['tag']=self.object.get_tag().values_list('id',flat=True)
    
        return self.initial
        
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.author=self.request.user;
        self.object.save()
        tag_save.send(sender=GrouperCreateView,  parent = self.object, tag=form.cleaned_data.get('tag'))
        return HttpResponseRedirect("/")    

     #to powinno byc w inicie, ale nie moge zwalczyc gdzie jest tworzone 
    def get_context_data(self, **kwargs):
        context = super(GrouperUpdateView, self).get_context_data(**kwargs)
         #kady views powinine to wyrzycac jesli maja byc widoczne tagi jako menu w sidebarze
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        return context



class ArticleDeleteView(RegionViewMixin, DeleteView):
    model = get_model('epapyrus', 'Article')
    
    form_class = forms.CreateArticle
    success_url = '/'
 
 
    def get_object(self, queryset=None):
        obj = super(ArticleDeleteView, self).get_object(queryset);
        if self.request.user != obj.author:
            raise Http404
        return obj
   
    def get_context_data(self, **kwargs):
        context = super(ArticleDeleteView, self).get_context_data(**kwargs)
        context['region_postfixes'] = {'content': 'delete'}
        return context
        
        
    # znowu klopot bo delete robi redirecta co niekoniecznie musi byc poprawne
    # a wiec najpier wysgnal a potem 
    
    
    def post(self, *args, **kwargs):
        if args[0].POST.has_key('Cancel'):
           return HttpResponseRedirect("/article/%d/" % self.get_object().id);
        else:
           obj_delete.send(sender=ArticleDeleteView,  obj = self.get_object())
           return self.delete(*args, **kwargs)


class NoteCreateView(RegionViewMixin, CreateView):
    model = get_model('epapyrus', 'Note')
    
    
    form_class = forms.CreateNoteForm
    
    def _get_content_object(self, model_name, obj_id):
        content_type = ContentType.objects.get(app_label="epapyrus", model=model_name)
        try:
            return content_type.get_object_for_this_type(id=obj_id)
            
        except ObjectDoesNotExist:
            raise Http404
         
    def get_initial(self):
        super(NoteCreateView, self).get_initial()
        
        self.object_for_note = self._get_content_object(self.kwargs['model_name'], self.kwargs['obj_id'])
        
        if self.object_for_note.author != self.request.user:
            raise Http404
        return self.initial
    
    def get_context_data(self, *args, **kwargs):
        context = super(NoteCreateView, self).get_context_data(*args, **kwargs)
        context['parent'] = self.object_for_note
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        
        return context
        
    def form_valid(self, form):
        
        
        self.object = form.save(commit=False)
        self.object.author=self.request.user;
        self.object.content_type = ContentType.objects.get_for_model(self.object_for_note)
        self.object.object_id = self.object_for_note.id
        self.object.save()
        return HttpResponseRedirect("/%s/%s/" % (self.object.content_type, self.object.object_id) )    


class NoteUpdateView(RegionViewMixin, UpdateView):
    model = get_model('epapyrus', 'Note')
    
    
    form_class = forms.CreateNoteForm
 
    
    def form_valid(self, form):
        self.object.note = form.cleaned_data.get('note')
        self.object.title = form.cleaned_data.get('title')
        self.object.save()
        return HttpResponseRedirect("/notes/%s/%s/" % (self.object.content_type, self.object.object_id) )    
    
    def get_context_data(self, *args, **kwargs):
        context = super(NoteUpdateView, self).get_context_data(*args, **kwargs)
        context['parent'] = self.object.content_object
        context['tags'] = get_model('epapyrus','PrimaryTagType').objects.all()
        
        return context

class NoteDeleteView(RegionViewMixin, DeleteView):
    model = get_model('epapyrus', 'Note')
    
   
   
    def get_success_url(self):
        return "/notes/%s/%s/" % (self.note_object.content_type, self.note_object.object_id)  
     
    def get_context_data(self, **kwargs):
        context = super(NoteDeleteView, self).get_context_data(**kwargs)
        context['region_postfixes'] = {'content': 'delete'}
        return context
    
    
    def post(self, *args, **kwargs):
        self.note_object = self.get_object();
        if args[0].POST.has_key('Cancel'):
           return HttpResponseRedirect(self.get_success_url());
        else:
           
           return self.delete(*args, **kwargs)    
           
           
           
#get tag signal after save
@receiver(tag_save)
def save_tag_content(sender, **kwargs):
   
    tag_item_model = get_model('epapyrus','PrimaryTagItem')
    model = ContentType.objects.get_for_model(kwargs['parent'])
    
    saved_tags = kwargs['parent'].get_tag() 
    entered_tags = kwargs['tag']
    
    #a moze tags_delete = list(set(saved_tags) - set(enetered_tags))
    tags_deleted = [ tag for tag in saved_tags if not tag in entered_tags ]
    tags_entered = [ tag for tag in entered_tags if not tag in saved_tags ]
            
    #delete tags that are unchecked
    tag_item_model.objects.filter(content_type__exact=model.pk, object_id__exact=kwargs['parent'].id,tag__in=tags_deleted).delete()
    #enter new tags
    for i in tags_entered:
        tag_item = tag_item_model(content_object=kwargs['parent'], tag=i)
        tag_item.save()
  
   
  

@receiver(obj_delete)
def tag_obj_delete(sender, **kwargs):
   
    tag_item_model = get_model('epapyrus','PrimaryTagItem')
    model = ContentType.objects.get_for_model(kwargs['obj'])
    tag_item_model.objects.filter(content_type__exact=model.pk, object_id__exact=kwargs['obj'].id).delete() 
 
