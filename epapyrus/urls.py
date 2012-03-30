# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from epapyrus.views  import simple, edit, listing, detail

urlpatterns = patterns('',
                       url(r'^$', listing.ArticlesView.as_view(), name='main'),
                       url(r'^article/add/$', login_required(edit.ArticleCreateView.as_view()), name='add_article'),
                       url(r'^article/(?P<pk>\d+)/$', detail.ArticleDetailView.as_view(), name='article'),
                       url(r'^article/(?P<pk>\d+)/edit/$', login_required(edit.ArticleUpdateView.as_view()), name='article_update'),
                       url(r'^article/(?P<pk>\d+)/delete/$', login_required(edit.ArticleDeleteView.as_view()), name='article_delete'),
                       
                       url(r'^grouper/add$', login_required(edit.GrouperCreateView.as_view()), name='add_grouper'),
                       url(r'^grouper/(?P<pk>\d+)/edit/$', login_required(edit.GrouperUpdateView.as_view()), name='grouper_edit'),
                       url(r'^grouper/(?P<pk>\d+)/delete/$', login_required(edit.GrouperDeleteView.as_view()), name='grouper_delete'),
                       
                       
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'epapyrus_skin/login.html'}, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

                       url(r'^tag/(?P<tag_code>\w+)/$', listing.TagView.as_view(), name="tag_view"),
                       url(r'^books/$',listing.BooksView.as_view(), name="books"),
                       url(r'^book/(?P<pk>\d+)/$',detail.GrouperView.as_view(), name="grouper_view"),
                       
                       url(r'^image/(?P<article>\d+)/add/$',login_required(edit.ArticleImageCreateView.as_view()), name="add_image"),
                       url(r'^file/(?P<article>\d+)/add/$',login_required(edit.ArticleFileCreateView.as_view()), name="add_file"),
                       url(r'^note/(?P<model_name>article|grouper)/(?P<obj_id>\d+)/create$',login_required(edit.NoteCreateView.as_view()), name="add_note"),
                       url(r'^note/(?P<pk>\d+)/update$',login_required(edit.NoteUpdateView.as_view()), name="note_update"),
                       url(r'^note/(?P<pk>\d+)/delete$',login_required(edit.NoteDeleteView.as_view()), name="note_delete"),
                       url(r'^notes/(?P<model_name>article|grouper)/(?P<obj_id>\d+)/$',login_required(listing.ShowNotes.as_view()), name="notes_view"),
                       )

