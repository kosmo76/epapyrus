# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import get_model

import markdown

# Create your models here.


class LanguageName(models.Model):
    name = models.CharField(max_length=100, verbose_name="Language", unique=True)
    machine_name = models.SlugField(max_length=10, verbose_name="Language code")
    
    def __unicode__(self):
        return u"%s" % self.name

class Grouper(models.Model):
    
    language = models.ForeignKey('LanguageName', verbose_name="Language", related_name="groupers");
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Creation time")
    modification_datetime = models.DateTimeField(auto_now = True, verbose_name="Modification time")
    
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    machine_name = models.SlugField(max_length=255, verbose_name="Machine name", unique=True)
    parent = models.ForeignKey('Grouper', verbose_name="Parent", related_name="groupers", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    note = models.TextField(verbose_name="Grouper note", blank=True)
    publish = models.BooleanField(verbose_name="Published", default=False)
    
        
    def __unicode__(self):
        return u"%s" % self.title
    
    
class Article(models.Model):
    
    language = models.ForeignKey('LanguageName', verbose_name='Language', related_name="articles");
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now = True)
    
    title = models.CharField(max_length=255, verbose_name="Title")
    machine_name = models.SlugField(max_length=255, verbose_name="Machine name", unique=True)
    body = models.TextField(verbose_name="Article body")
    teaser = models.TextField(verbose_name="Teaser", blank=True)
   
    parent = models.ForeignKey('Article', verbose_name="Parent", related_name="articles", null=True, blank=True)
    grouper = models.ForeignKey('Grouper', verbose_name="Grouper", related_name="articles", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    publish = models.BooleanField(verbose_name="Published", default=False)
        
    def __unicode__(self):
        return u"%s" % self.title

    def get_tag(self):
        article_model = ContentType.objects.get(app_label="osblog", model="article")
        article_tag= models.get_model('osblog', 'PrimaryTagItem').objects.filter(content_type__pk__exact=article_model.id, object_id__exact=self.id).values_list('tag', flat=True);
        return models.get_model('osblog','PrimaryTagType').objects.filter(id__in=article_tag)
        
    def get_test(self):
        return markdown.markdown(self.body,['codehilite(force_linenos=True)'])

        
class PrimaryTagType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tab name", unique=True)
    machine_name=models.SlugField(max_length=50, verbose_name="machine_name", unique=True)
    
    def __unicode__(self):
        return u"%s" % self.name
        

    
class PrimaryTagItemManager(models.Manager):
    
    def get_for_tag(self, tag):
        result = get_model('osblog','PrimaryTagItem').objects.filter(tag__name__exact=tag)
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

