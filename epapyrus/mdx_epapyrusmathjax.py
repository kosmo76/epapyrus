# -*- coding: utf-8 -*-
import markdown
from markdown.inlinepatterns import Pattern
#from markdown import etree

BLOCK_MATH_RE = r'\${2}([^$]+)\${2}'
INLINE_MATH_RE = r'\\\(([^)]+)\\\)'

class EpapyrusMathJaxPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3) 
    of a Pattern and with the html attributes defined with the constructor.

    """
    def __init__ (self, pattern, open_tag, close_tag):
        Pattern.__init__(self, pattern)
        self.open_tag = open_tag
        self.close_tag = close_tag

    def handleMatch(self, m):
        #Teoretycznie tu powinnien byc, element z etree, ale dzial chyba bez tego
        #el = markdown.etree.Element('<kosmo>')
        #el.text = markdown.AtomicString(m.group(2))
        #w innym wypadku trzeba stworzyc wlasny tag i potem ewentualnie go wywalic, ale ladne to to nie jest 
       
        text = markdown.util.AtomicString(m.group(2))
        return self.open_tag + text + self.close_tag

class EpapyrusMathJaxExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern_inline= EpapyrusMathJaxPattern(INLINE_MATH_RE,'\(','\)')
        md.inlinePatterns.add('epap_mathjax_inline', pattern_inline,"<escape") #ostatniego elementu nie kumam do konca 
        
        pattern_block= EpapyrusMathJaxPattern(BLOCK_MATH_RE,'$$','$$')
        md.inlinePatterns.add('epap_mathjax_block', pattern_block,"<escape")
        
        
def makeExtension(configs=None):
    return  EpapyrusMathJaxExtension(configs=configs)


