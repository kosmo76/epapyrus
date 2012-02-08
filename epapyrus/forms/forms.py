# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.shortcuts import get_object_or_404
from django import forms



from epapyrus import models


class CreateArticle(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField( get_model('epapyrus', 'PrimaryTagType').objects.all() )
    
    class Meta:
        model = models.Article
        exclude = ('author')
 
    #def save(self, force_insert=False, force_update=False, commit=True):
        #print "Poszedl save"
        #m = super(CreateArticle, self).save(commit=False)
        #print m.id
        #tag_save.send(sender=CreateArticle,  arg1=self.cleaned_data.get('tag')) 
        
        #return m
    
class CreateGrouper(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField( get_model('epapyrus', 'PrimaryTagType').objects.all() )
    
    class Meta:
        model = models.Grouper
        exclude = ('author')
        
        
