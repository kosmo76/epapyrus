# -*- coding: utf-8 -*-
from models import *
from django.contrib import admin



admin.site.register(Grouper)
admin.site.register(Article)

admin.site.register(PrimaryTagType)
admin.site.register(PrimaryTagItem)
admin.site.register(ArticleImage)
admin.site.register(Note)