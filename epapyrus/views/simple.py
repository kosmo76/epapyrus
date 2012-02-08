# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

class MainView(TemplateView):
    template_name="epapyrus/main.html"
    
    
    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['cos']="querty gsdkl "
        return context