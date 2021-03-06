# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import get_model
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import re
import os
import datetime
import markdown
import mdx_epapyrusmathjax as mathjax
import mdx_epapcode as ecode




files_location = os.path.join(settings.MEDIA_ROOT)
file_system_storage = FileSystemStorage(location=files_location, base_url=settings.MEDIA_URL) 

def image_save(instance, filename):
    personal = instance.article.id
    return  os.path.join("%s" % instance.article.id,'images', '%s'%filename)
 

def file_save(instance, filename):
    personal = instance.article.id
    return  os.path.join("%s" % instance.article.id,'files', '%s'%filename) 

class GrouperManager(models.Manager):

    def get_books(self):
        """ Return the groupers having no parent. """
        return self.filter(parent__isnull=True)

    def get_authored_books(self, author):
        """ Retrns public groupers having no parent. """
        return self.get_books().filter(author=author)

    def get_public(self):
        """ Returns only public groupers. """
        return self.filter(is_published=True)

    def get_public_books(self):
        """ Retrns public groupers having no parent. """
        return self.get_public().filter(parent__isnull=True)


class Grouper(models.Model):
    
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Creation time")
    modification_datetime = models.DateTimeField(auto_now = True, verbose_name="Modification time")
    
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    parent = models.ForeignKey('Grouper', verbose_name="Parent", related_name="groupers", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    note = models.TextField(verbose_name="Grouper note", blank=True)
    is_published = models.BooleanField(verbose_name="Publish", default=False)
    
    objects = GrouperManager()
        
    def __unicode__(self):
        return u"%s" % self.title
    
    def get_articles(self):
        return get_model('epapyrus','Article').objects.filter(grouper__exact = self)
        
    def get_groupers(self):
        return get_model('epapyrus','Grouper').objects.filter(parent__exact = self)
    
    def get_tag(self):
        grouper_model = ContentType.objects.get(app_label="epapyrus", model="grouper")
        grouper_tag= models.get_model('epapyrus', 'PrimaryTagItem').objects.filter(content_type__pk__exact=grouper_model.id, object_id__exact=self.id).values_list('tag', flat=True);
        return models.get_model('epapyrus','PrimaryTagType').objects.filter(id__in=grouper_tag)
        

    class Meta:
        ordering = ('weight', 'creation_datetime', 'title')

class ArticleManager(models.Model):
    
    def get_authored(self, author):
        """ Retrns public groupers having no parent. """
        return self.filter(author=author)

    def get_public(self):
        """ Returns only public groupers. """
        return self.filter(is_published=True)

class Article(models.Model):
    
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now = True)
    
    title = models.CharField(max_length=255, verbose_name="Title")

    body = models.TextField(verbose_name="Article body")
    teaser = models.TextField(verbose_name="Teaser", blank=True)
    extras = models.TextField(verbose_name="Reference for Markdown", blank=True)
   
    grouper = models.ForeignKey('Grouper', verbose_name="Grouper", related_name="articles", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    is_published = models.BooleanField(verbose_name="Publish", default=False)
    is_promoted = models.BooleanField(verbose_name="Promote", default=False)
    

    objects = ArticleManager()
    
    def __unicode__(self):
        return u"%s" % self.title

    def _find_parent(self, grouper):
        k=grouper
        if grouper.parent != None:
            k = self._find_parent(grouper.parent)
            
        return k
        
        
    def get_root(self):
        if self.grouper != None:
            w = self._find_parent(self.grouper)
            return w
        return None
    
    def get_tag(self):
        article_model = ContentType.objects.get(app_label="epapyrus", model="article")
        article_tag= models.get_model('epapyrus', 'PrimaryTagItem').objects.filter(content_type__pk__exact=article_model.id, object_id__exact=self.id).values_list('tag', flat=True);
        return models.get_model('epapyrus','PrimaryTagType').objects.filter(id__in=article_tag)
    
    def has_notes(self):
        article_model = ContentType.objects.get(app_label="epapyrus", model="article")
        note_model = get_model('epapyrus', 'Note').objects.filter(content_type__pk__exact=article_model.id, object_id__exact=self.id).exists()
        return note_model
    

    def get_test(self):
        #uwaga trzebaby wyparsowac to locale !!!
        extras_user =  extras = self.extras.replace('locale://',settings.MEDIA_URL)
        extras_images = self.get_images_ref()
        extras_files = self.get_files_ref()
        
        extras = extras_images + extras_files + extras_user
        print extras
        myext = mathjax.EpapyrusMathJaxExtension()
        myext2 = ecode.EpapCodeExtension()
        
        md = markdown.Markdown(extensions=[myext2,myext,'codehilite'])
        return  md.convert(extras + self.body)
        

    def get_images_ref(self):
        ref=""
        for image in self.article_images.all():
            ref = "%s\n[im%d]: %s" %(ref, image.id, image.attachment.url)
        
        ref = "%s\n" % ref
        return ref
    
    class Meta:
        ordering = ('weight', 'creation_datetime', 'title')

    def get_files_ref(self):
        ref=""
        for i in self.article_files.all():
            ref = "%s\n[file%d]: %s" %(ref, i.id, i.attachment.url)
        
        ref = "%s\n" % ref
        return ref
    
        
class PrimaryTagType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tab name", unique=True)
    code=models.SlugField(max_length=50, verbose_name="code", unique=True)
    
    def __unicode__(self):
        return u"%s" % self.name
        

    
class PrimaryTagItemManager(models.Manager):
    
    def get_for_tag(self, tag, model):
        content_type = ContentType.objects.get(app_label='epapyrus', model=model)
        result_ids = get_model('epapyrus', 'PrimaryTagItem').objects.filter(tag__code__exact=tag, content_type=content_type).values_list('object_id', flat=True)
        return get_model('epapyrus', model).objects.filter(id__in=result_ids)

    def get_public_for_tag(self, tag, model):
        return self.get_for_tag(tag, model).filter(is_published=True)

    def get_authored_for_tag(self, tag, model, author):
        return self.get_for_tag(tag, model).filter(author=author)

        
class PrimaryTagItem(models.Model):
    tag = models.ForeignKey('PrimaryTagType', verbose_name="Primary tag", related_name="primary_tag_items")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = PrimaryTagItemManager()
    def __unicode__(self):
        return u"%s" % self.tag

class ArticleImage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    article = models.ForeignKey('Article', verbose_name = "Article", related_name="article_images")
    attachment = models.ImageField(verbose_name="Image", storage = file_system_storage, upload_to = image_save, )
 
    def delete(self, *args, **kwargs):
        image_path = os.path.join( self.attachment.file.name)
        os.remove(image_path)
        self.attachment.delete()
        
        super(ArticleImage, self).delete(*args, **kwargs)
        
class ArticleFile(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    article = models.ForeignKey('Article', verbose_name = "Article", related_name="article_files")
    attachment = models.FileField(verbose_name="File", storage = file_system_storage, upload_to = file_save)
 
    def delete(self, *args, **kwargs):
        file_path = os.path.join( self.attachment.file.name)
        os.remove(file_path)
        self.attachment.delete()
        
        super(ArticleFile, self).delete(*args, **kwargs)
        
#model reprezentujacy notatke do artykulu lub groupera
class Note(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    modification_datetime = models.DateTimeField(auto_now = True, verbose_name="Modification time")
    author = models.ForeignKey('auth.User', verbose_name="Author")
    note =  models.TextField(verbose_name="Note")
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in':['article','grouper']})
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    #chyba nie bedzie potrzebne jednak
    def get_teaser(self):
        tmp = self.note.split()
        result =  " ".join([ i for i in tmp[0:20]])
        if len(tmp) > 19:
            result = result + " (...) "
        
        return result
    def get_safe(self):
        return markdown.markdown( self.note )
        
