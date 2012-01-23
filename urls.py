# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from osblog.views  import simple, edit, listing, detail

urlpatterns = patterns('',
                       url(r'^main/$', listing.ArticlesView.as_view(), name='main'),
                       url(r'^article/add/$', login_required(edit.ArticleCreateView.as_view()), name='article_add'),
                       url(r'^article/(?P<pk>\d+)/$', detail.ArticleDetailView.as_view(), name='article'),
                       url(r'^article/(?P<pk>\d+)/edit/$', login_required(edit.ArticleUpdateView.as_view()), name='article_update'),
                       url(r'^article/(?P<pk>\d+)/delete/$', login_required(edit.ArticleDeleteView.as_view()), name='article_delete'),
                       
                       url(r'^grouper/add$', login_required(edit.GrouperCreateView.as_view()), name='grouper_add'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'osblog/login.html'}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/main/'},name='logout'),

                       url(r'^tag/(?P<tag_name>Programming|C\+\+|C|Pyton)/$',listing.TagView.as_view(), name="tag_view"),
                       ## Uncomment the admin/doc line below to enable admin documentation:
                        #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       ## Uncomment the next line to enable the admin:
                       #url(r'^admin/', include(admin.site.urls)),
                       )

