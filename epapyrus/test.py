# -*- coding: utf-8 -*-
import markdown

md = markdown.Markdown(extensions=['epapyrusmathjax'])
print md.convert(r'To jest cos $$ \alpha 2**2** $$\( \beta 2_2 **3**\)lskds')
