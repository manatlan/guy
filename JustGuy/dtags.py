#!/usr/bin/python3 -u
import sys,os; sys.path.insert(0,os.path.dirname(__file__)+"/..")

import html
import guy

"""
    Working on this

    (will replace guycompo & co)

    use guy >=0.7.2 !
"""

#~ from react import ReactiveProp

class ReactiveProp:
    def __init__(self,instance,attribut:str):
        # assert attribut in instance.__dict__.keys()
        self.instance=instance
        self.attribut=attribut
    def set(self,v):
        self.instance.__dict__[self.attribut]=v
    def get(self):
        return self.instance.__dict__[self.attribut]

    def __eq__(self,v):
        return self.get() == v
        
    def __int__(self):
        return int(self.get())

    def __add__(self,v): # add in place
        vv=self.get() + v
        self.set( vv )
        return self

    def __str__(self):
        return str(self.get())
        
    def __repr__(self):
        return "<%s instance=%s attr=%s>" % (self.__class__.__name__,self.instance.id,self.attribut)
    #TODO: add a lot of __slot__ ;-)




class Tag:
    tag="div" # default one
    klass=None

    def __init__(self,*contents,**attrs):
        assert "id" not in attrs.keys()
        self.id=None
        self.tag=self.__class__.tag
        self.contents=list(contents)
        if "klass" in attrs:
            attrs["class"]=attrs["klass"]
            del attrs["klass"]
        else:
            if self.klass:
                attrs["class"]=self.klass
            else:
                attrs["class"]=self.__class__.__name__.lower()

        self.attrs=attrs
        self.attrs={k.replace("_","-"):v for k,v in self.attrs.items()}

    def add(self,o):
        self.contents.append(o)

    def __str__(self):
        attrs=self.attrs
        if self.id: attrs["id"]=self.id
        attrs=['%s="%s"'%(k if k!="klass" else "class",html.escape( str(v) )) for k,v in attrs.items()]
        return """<%(tag)s %(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag,
            attrs=" ".join(attrs),
            content=" ".join([str(i) for i in self.contents]),
        )

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


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

class Section(Tag):
    tag="section"
class Nav(Tag):
    tag="nav"
    klass="navbar is-fixed-top is-black"

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
    klass="button is-light"
class Ul(Tag):
    tag="ul"
class Li(Tag):
    tag="li"

#################################

class App(guy.Guy):
    size=(400,300)

    def __init__(self,app):
        super().__init__()
        self._tag=app

    def render(self,path=None):
        return """<!DOCTYPE html>
        <html>
            <head>
                <script>
                if(!sessionStorage["gid"]) sessionStorage["gid"]=Math.random().toString(36).substring(2);
                var GID=sessionStorage["gid"];
                
                async function launchApp() {    // NOT USED YET !!
                    await self.startApp(GID);
                }
                </script>
            
                <script src="guy.js"></script>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">

                <style>
                div.hbox {display: flex;flex-flow: row nowrap;align-items:center }
                div.vbox {display: flex;flex-flow: column nowrap;}
                div.hbox > *,div.vbox > * {flex: 1 1 50%%;margin:1px}
                </style> 
            </head>
            <body>%s</body>
        </html>
        """ % self._tag
        
    def bindUpdate(self,id:str,method:str,*args):
        obj=self._tag.getInstance(id)
        r=getattr(obj,method)(*args)
        return self.update()    # currently it update all ;-(
        
    def update(self):
        """ Exposed in py/side !"""
        return self._tag.update()
        
        



class DTag:
    _dtags={}
    def __init__(self):
        self.id="%s_%s" % (self.__class__.__name__,id(self))
        DTag._dtags[self.id]=self       # maj une liste des dynamic created

        self._tag = self.build()

    def build(self):
        """ Override for static build 
            SHOULD RETURN a "Tag" (not a DTag)
        """
        return None

    def render(self):
        """ Override for dynamic build 
            SHOULD RETURN a "Tag" (not a DTag)
        """
        return None

    def __str__(self):
        if self._tag is None:
            o=self.render()
            assert o,"'%s' doesn't have a build or a render methods ?!" % self.__class__.__name__
        else:
            o=self._tag
            assert self.render() is None, "'%s' has already builded its component ?!" % self.__class__.__name__
        assert not isinstance(o,DTag), "'%s' produce a DTag, wtf?!" % self.__class__.__name__ # because it's a non-sense that a Dtag return a Dtag .. that's all!
        o.id=self.id
        return str(o)


    def getInstance(self,id):
        return DTag._dtags[id]

    def __setattr__(self,k,v):
        current="%s_%s" % (self.__class__.__name__,id(self))
        o=self.__dict__.get(k)
        if isinstance(o,ReactiveProp):
            # print("Maj %s ReactProp %s <- %s" % (current,k,repr(v)))
            if isinstance(v,ReactiveProp):
                self.__dict__[k]=v
            else:
                o.set(v)
        else:
            # print("Maj %s Prop %s <- %s" % (current,k,repr(v)))
            super().__setattr__(k,v)

    @property
    def bind(self):
        """ to bind attribute or method !"""
        class Binder:
            def __getattr__(sself,name):
                if name in self.__dict__.keys(): # bind a data attribut  -> return a ReactiveProp
                    o=self.__dict__[name]
                    if isinstance(o,ReactiveProp):
                        return o
                    else:
                        return ReactiveProp(self,name)
                elif name in dir(self):   # bind a self.method    -> return a js/string for a guy's call in js side
                    def _(*args):
                        if args:
                            return "self.bindUpdate('%s','%s',%s)" % (self.id,name,",".join([str(i) for i in args]) ) #TODO: escaping here ! (and the render/str ?) json here !
                        else:
                            return "self.bindUpdate('%s','%s')" % (self.id,name)
                    return _
                else:
                    raise Exception("Unknown method/attribut '%s' in '%s'"%(name,self.__class__.__name__))
        return Binder()        

    def update(self):
        print("update:"+self.id)
        return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (
            self.id, self
        ))


    def run(self,*a,**k):
        app=App(self)
        self.exit=app.exit
        return app.run(*a,**k)


############################################################################################################
############################################################################################################
############################################################################################################

class Inc(DTag):
    def __init__(self,v=0):
        self.cpt=v
        super().__init__()
        
    def build(self):    # called at __init__()
        return HBox(
                Button("-",onclick=self.bind.addV(-1) ),         #<- bind GuyCompo event
                Text(self.bind.cpt,style="text-align:center"),
                Button("+",onclick=self.bind.addV(1) ),          #<- bind GuyCompo event
            )
        

    def addV(self,v):
        self.cpt+=v


class MyInput(DTag):

    def __init__(self,txt):
        self.v=txt
        super().__init__()

    def build(self):
        return Input(type="text",value=self.v,onchange=self.bind.onchange("this.value"))

    def onchange(self,txt):
        self.v = txt
        

        
class MyTabs(DTag):

    def __init__(self,selected:int,tabs:list):
        self.selected=selected
        self.tabs=tabs
        super().__init__()

    def render(self): # dynamic rendering !
        o = Tabs( )
        for idx,t in enumerate(self.tabs):
            o.addTab( self.selected==idx+1, t, onclick=self.bind.select(idx+1) ) 
        return o

    def select(self,idx):
        self.selected=idx

        
class DynCreate(DTag):
    def __init__(self,n):
        self.n=n
        super().__init__()
    def render(self):
        b=Box()
        for i in range( int(self.n) ):
            b.add(Inc(i))
        return b

class Page1(DTag):
    
    def __init__(self):
        self.nb=12
        self.txt="yolo"
        self.selected=2
        super().__init__()
    
    def build(self):    # called at __init__()
        return VBox(
            MyInput( self.bind.txt ),
            Text(self.bind.txt,self.bind.selected),
            Inc(self.bind.nb),
            Inc(self.bind.nb),
            Inc(self.nb),
            Inc(13),
            Box(self.bind.nb),
            DynCreate(self.bind.nb),
            MyTabs(self.bind.selected,["johan","jim"]),
        )

class Page2(DTag):
    
    def __init__(self):
        self.nb=12
        super().__init__()
    
    def build(self):    # called at __init__()
        return VBox(
            Box("A test page, with a binding value:", self.bind.nb),
            Inc(self.bind.nb),
        )

        
        
   

class TestApp(DTag):
    def __init__(self):
        self.obj=Page1()
        super().__init__()

    def render(self):
        divBrand=Div( klass="navbar-brand" )
        divBrand.add( A("<b>MYAPP</b>",klass="navbar-item") )
        divBrand.add( A('<span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>',
                        role="button",
                        klass="navbar-burger burger",
                        aria_label="menu",
                        aria_expanded="false",
                        data_target="navbarBasicExample",
                        onclick="this.classList.toggle('is-active');document.querySelector('.navbar-menu').classList.toggle('is-active')") )

        divMenu=Div( klass="navbar-menu" )
        menu=Div(klass="navbar-start")
        menu.add( A("Page1", klass="navbar-item",onclick=self.bind.setPage1() ))
        menu.add( A("Page2", klass="navbar-item",onclick=self.bind.setPage2() ))
        menu.add( A("Exit", klass="navbar-item", onclick=self.bind.doExit() ) )
        divMenu.add( menu )

        return Body(
            Nav( divBrand, divMenu, role="navigation",aria_label="main navigation"),
            Section( Div( "<br>", self.obj, klass="container") ),
        )

    def doExit(self):
        self.exit(-1)

    def setPage1(self):
        self.obj=Page1()

    def setPage2(self):
        self.obj=Page2()

if __name__=="__main__":
    #~ b=Body("hello",onload="hello()")
    #~ assert repr(b)=='<body onload="hello()" class="body">hello</body>'

    #~ x=DTag()
    #~ print(x)

    # tag=Multi()
    tag=TestApp()
    #~ print(tag)
    #~ print(tag.render())
    #~ quit()
    
    print( tag.run() )
    