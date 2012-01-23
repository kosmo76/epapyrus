# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import markdown

# Create your models here.



class Grouper(models.Model):
    
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
    
    author = models.ForeignKey('auth.User', verbose_name="Author")
    creation_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now = True)
    
    title = models.CharField(max_length=255, verbose_name="Title")
    body = models.TextField(verbose_name="Article body")
    teaser = models.TextField(verbose_name="Teaser", blank=True)
    machine_name = models.SlugField(max_length=255, verbose_name="Machine name", unique=True)
    parent = models.ForeignKey('Article', verbose_name="Parent", related_name="articles", null=True, blank=True)
    grouper = models.ForeignKey('Grouper', verbose_name="Grouper", related_name="articles", null=True, blank=True)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    publish = models.BooleanField(verbose_name="Published", default=False)
        
    def __unicode__(self):
        return u"%s" % self.title

    def get_tag(self):
        article_model = ContentType.objects.get(app_label="osblog", model="article")
        article_tag= models.get_model('osblog', 'PrimaryTagItem').objects.filter(content_type__pk__exact=article_model.id, object_id__exact=self.id);
        if len(article_tag) > 0:
            return article_tag[0].tag
        return None;
        
    def get_test(self):
        return markdown.markdown(self.body,['codehilite(force_linenos=True)'])

        
class PrimaryTagType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tab name", unique=True)
    machine_name=models.SlugField(max_length=50, verbose_name="machine_name", unique=True)
    
    def __unicode__(self):
        return u"%s" % self.name
        

class PrimaryTagItem(models.Model):
    tag = models.ForeignKey('PrimaryTagType', verbose_name="Primary tag", related_name="primary_tag_items")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return u"%s" % self.tag

    #chyba uniq na tag, cintent_type, object_id

    