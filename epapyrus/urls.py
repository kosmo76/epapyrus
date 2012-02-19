# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from epapyrus.views  import simple, edit, listing, detail

urlpatterns = patterns('',
                       url(r'^$', listing.ArticlesView.as_view(), name='main'),
                       url(r'^article/add/$', login_required(edit.ArticleCreateView.as_view()), name='article_add'),
                       url(r'^article/(?P<pk>\d+)/$', detail.ArticleDetailView.as_view(), name='article'),
                       url(r'^article/(?P<pk>\d+)/edit/$', login_required(edit.ArticleUpdateView.as_view()), name='article_update'),
                       url(r'^article/(?P<pk>\d+)/delete/$', login_required(edit.ArticleDeleteView.as_view()), name='article_delete'),
                       
                       url(r'^grouper/add$', login_required(edit.GrouperCreateView.as_view()), name='grouper_add'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'epapyrus/login.html'}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': ''},name='logout'),

                       url(r'^tag/(?P<tag_code>programming|cpp|c|python)/$', listing.TagView.as_view(), name="tag_view"),
                       url(r'^books/$',listing.BookView.as_view(), name="book_view"),
                       url(r'^image/(?P<article>\d+)/add/$',login_required(edit.ArticleImageCreateView.as_view()), name="add_image"),
                       ## Uncomment the admin/doc line below to enable admin documentation:
                        #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       ## Uncomment the next line to enable the admin:
                       #url(r'^admin/', include(admin.site.urls)),
                       )

