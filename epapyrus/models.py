# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import get_model

import markdown
import re

# Create your models here.

class Grouper(models.Model):
    
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Creation time")
    modification_datetime = models.DateTimeField(auto_now = True, verbose_name="Modification time")
    
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    parent = models.ForeignKey('Grouper', verbose_name="Parent", related_name="groupers", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    note = models.TextField(verbose_name="Grouper note", blank=True)
    is_published = models.BooleanField(verbose_name="Publish", default=False)
    
        
    def __unicode__(self):
        return u"%s" % self.title
    
    
class Article(models.Model):
    
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now = True)
    
    title = models.CharField(max_length=255, verbose_name="Title")

    body = models.TextField(verbose_name="Article body")
    teaser = models.TextField(verbose_name="Teaser", blank=True)
    footer = models.TextField(verbose_name="References", blank=True)
   
    grouper = models.ForeignKey('Grouper', verbose_name="Grouper", related_name="articles", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    is_published = models.BooleanField(verbose_name="Publish", default=False)
    is_promoted = models.BooleanField(verbose_name="Promote", default=False)
        
    def __unicode__(self):
        return u"%s" % self.title

    def get_tag(self):
        article_model = ContentType.objects.get(app_label="epapyrus", model="article")
        article_tag= models.get_model('epapyrus', 'PrimaryTagItem').objects.filter(content_type__pk__exact=article_model.id, object_id__exact=self.id).values_list('tag', flat=True);
        return models.get_model('epapyrus','PrimaryTagType').objects.filter(id__in=article_tag)
        
    def get_test(self):
        napis = self.footer + self.body
        #regexp = re.compile(r"\$\$([^$]+)\$\$",re.UNICODE)
        regexp = re.compile(r"\${1,2}([^$]+)\${1,2}",re.UNICODE)
        
        r = regexp.search(napis)
        dane = regexp.finditer(napis)
        start=0
        
        nowy=""
        for i in  dane:
            end=i.start()
            nowy += markdown.markdown( self.footer+napis[start:end] ,['codehilite(force_linenos=True)'])
            nowy += napis[i.start():i.end()]+" "
            start=i.end()
        nowy += markdown.markdown(self.footer+napis[start:],['codehilite(force_linenos=True)'])
        return nowy

        
class PrimaryTagType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tab name", unique=True)
    code=models.SlugField(max_length=50, verbose_name="code", unique=True)
    
    def __unicode__(self):
        return u"%s" % self.name
        

    
class PrimaryTagItemManager(models.Manager):
    
    def get_for_tag(self, tag):
        result = get_model('epapyrus','PrimaryTagItem').objects.filter(tag__code__exact=tag)
        wynik = [ x.content_object for x in result ]
        return wynik
        
        
class PrimaryTagItem(models.Model):
    tag = models.ForeignKey('PrimaryTagType', verbose_name="Primary tag", related_name="primary_tag_items")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = PrimaryTagItemManager()
    def __unicode__(self):
        return u"%s" % self.tag

