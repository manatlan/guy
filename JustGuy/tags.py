#!/usr/bin/python3 -u
import html
"""
    inferface between HTML rendering (BULMA.css oriented)
"""

from react import ReactiveProp


def render(c: any) -> str: 
    if hasattr(c,"render"): # better here ? (c is GuyCompo like)
        return c.render(False)
    elif isinstance(c,ReactiveProp):
        return str(c.get())
    else:
        return str(c)   

class Tag:
    tag="div" # default one
    klass=None
    def __init__(self,*contents,**attrs):
        self.tag=self.__class__.tag
        self.contents=list(contents)
        self.attrs=attrs
        self.attrs["class"]=self.klass if self.klass else self.__class__.__name__.lower()
    def add(self,o):
        self.contents.append(o)
    def __repr__(self):
        attrs=['%s="%s"'%(k if k!="klass" else "class",html.escape( render(v) )) for k,v in self.attrs.items()]
        return """<%(tag)s %(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag,
            attrs=" ".join(attrs),
            content=" ".join([render(i) for i in self.contents]),
        )
    def render(self,full=False):
        if full:
            return """<script src="guy.js"></script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">

<style>
div.hbox {display: flex;flex-flow: row nowrap;align-items:center }
div.vbox {display: flex;flex-flow: column nowrap;}
div.hbox > *,div.vbox > * {flex: 1 1 50%%;margin:1px}
</style> <body>%s</body>""" % self
        else:
            return str(self)

class Body(Tag): 
    tag="body"

class Input(Tag): 
    tag="input"
class A(Tag): 
    tag="a"
class Box(Tag): 
    klass="box"
class Div(Tag):  pass

class HBox(Tag): pass
# class HBox(Tag):
#     tag="div"
#     klass="columns is-mobile"
#     def __init__(self,*contents,**attrs):
#         super().__init__(**attrs)
#         self.contents=[Div(i,klass="column") for i in list(contents)]
#     def add(self,o):
#         self.contents.append( Div(o,klass="column"))


class VBox(Tag): pass
class Tabs(Tag):
    klass="tabs is-centered"
    def __init__(self,**attrs):
        super().__init__(*attrs)
        self.ul=Ul()
        self.contents.append( self.ul )
    def addTab(self,selected,title,onclick=None):
        if selected:
            self.ul.add( Li(A(title,onclick=onclick), klass="is-active" ) )
        else:
            self.ul.add( Li(A(title,onclick=onclick)) )

class Text(Tag):
    tag="p"
class Button(Tag):
    tag="button"
    klass="button is-light "
class Ul(Tag):
    tag="ul"
class Li(Tag):
    tag="li"

if __name__=="__main__":
    b=Body("hello",onload="hello()")
    assert repr(b)=='<body onload="hello()" class="body">hello</body>'