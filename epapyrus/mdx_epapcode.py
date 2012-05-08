# -*- coding: utf-8 -*-
import markdown
import re
from markdown.inlinepatterns import Pattern
from markdown.preprocessors import Preprocessor

#from markdown import etree

BLOCK_CODE_RE = r'\[code\](.+)\[/code\]'

class EpapyrusCodePattern(Preprocessor):
    def run(self, lines):
        prog = re.compile(BLOCK_CODE_RE)

        try:
            start = lines.index('[code]')
            end =  lines.index('[/code]')
            for i in range(start+1,end):
                lines[i] = '    '+lines[i]
            del lines[end]
            del lines[start]
          
        except ValueError:
            pass
        
        return lines


class EpapCodeExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern=EpapyrusCodePattern()
        md.preprocessors.add('epapcode',pattern,'_begin')
        
        
def makeExtension(configs=None):
    return EpapCodeExtension(configs=configs)


