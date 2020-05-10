#!/usr/bin/python3 -u
import guy,os,html

""" A lot Inspired by Vue syntax ! 

At the beginning, it was just a test to try to reproduce with "Guy", things like :
- justpy
- https://www.reddit.com/r/Python/comments/gfq5ik/i_wrote_a_new_ui_framework_inspired_by_flutter/
- flutter

But things going better and better ... without too magical things
Helped by the vuejs concepts: it's now a lot more than a toy
And so : it could clearly the future of "Guy Components" ;-)
(which could be a "VuePy" server side)
"""

####################################################################################
## here are the base (surclass guy)
####################################################################################

class ReactiveProp:
    def __init__(self,instance,attribut):
        self.instance=instance
        self.attribut=attribut
    def set(self,v):
        self.instance._data[self.attribut]=v
    def get(self):
        return self.instance._data[self.attribut]


class DictReactiveProp:
    def __init__(self,d):
        self._data=d
    def __setitem__(self,k,v):
        g=ReactiveProp(self,k)
        g.set(v)
    def __getitem__(self,k):
        g=ReactiveProp(self,k)
        return g.get()
    def items(self):
        for k in self._data.keys():
            yield k,ReactiveProp(self,k)


def render(c: any) -> str: 
    if isinstance(c,GuyCompo):
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


class Input(Tag): 
    tag="input"
class Link(Tag): 
    tag="a"
class Box(Tag): 
    klass="box"
class Div(Tag):  pass
class HBox(Tag): pass
class VBox(Tag): pass
class Tabs(Tag):
    klass="tabs is-centered"
    def __init__(self,**attrs):
        super().__init__(*attrs)
        self.ul=Ul()
        self.contents.append( self.ul )
    def addTab(self,selected,title,onclick=None):
        if selected:
            self.ul.add( Li(Link(title,onclick=onclick), klass="is-active" ) )
        else:
            self.ul.add( Li(Link(title,onclick=onclick)) )

class Text(Tag):
    tag="p"
class Button(Tag):
    tag="button"
    klass="button is-light "
class Ul(Tag):
    tag="ul"
class Li(Tag):
    tag="li"


class GuyCompo(guy.Guy):
    
    @property
    def data(self): # MUTABLE !
        if not hasattr(self,"_data"): self._data={}
        class DataBinder:
            def __setattr__(zelf,k,v):
                o=self._data.get(k)
                if o and isinstance(o,ReactiveProp):
                    o.set(v)
                else:
                    self._data[k]=v
            def __getattr__(zelf,k):
                o=self._data[k]
                if isinstance(o,ReactiveProp):
                    return o.get()
                else:
                    return o
        return DataBinder()

    @property
    def dataBind(self): # retrun a ReactiveProp
        class Binder:
            def __getattr__(sself,attribut):
                assert attribut in self._data.keys(),"Unknown attribut '%s'"%attribut
                o=self._data[attribut]
                if isinstance(o,dict):
                    return DictReactiveProp(o)
                elif isinstance(o,DictReactiveProp) or isinstance(o,ReactiveProp):
                    return o
                else:
                    return ReactiveProp(self,attribut)
        return Binder()


    def bindUpdate(self,id:str,method:str,*args):
        # try to find the instance 'id'
        zelf=guy.Guy._instances.get(id)
        if zelf is None: raise Exception("can't find instance:"+id)
        # try to find the method in the instance
        if not hasattr(zelf,method):
            raise Exception("can't find method %s in %s"%(method,id))
        else:
            # call the method
            self._caller(getattr(zelf,method),args)
            
            return self.update() # and update all the content
            ########################################################################
            ## Currently, it's update all (so two ways binding works ootb)
            ## But in the future, the solution below is better 
            ## but should introduce a way to update everywhere where there
            ## are associate bindings !
            ## (replace the "return self.update()" ^^, with bellow)
            ########################################################################
            # print("bindUpdate:"+id)
            # return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (	
            #     id, self._caller( zelf.build ).render(False)	
            # ))	
            ########################################################################


    def update(self):
        print("update:"+self._id)
        return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (
            self._id, self.build().render(False)
        ))



    def _caller(self,method:str,args=[]):
        isBound="bound method" in str(method)
        if isBound:
            r=method(*args)
        else:
            r=method(self, *args)
        return r


    @property
    def bind(self):
        class Binder:
            def __getattr__(sself,method):
                assert method in self._routes.keys(),"Unknown method '%s'"%method
                def _(*args):
                    if args:
                        return "self.bindUpdate('%s','%s',%s)" % (self._id,method,",".join([render(i) for i in args]) ) #TODO: escaping here ! (and the render/str ?) json here !
                    else:
                        return "self.bindUpdate('%s','%s')" % (self._id,method)
                return _
        return Binder()

    def render(self,path): # path is FAKED (by true/false) #TODO
        d=Div(id=self._id)
        d.add( self._caller( self.build ) )
        return d.render(path)


####################################################################################
## here come the tests
####################################################################################
AHOUSE=dict(cat=3,dog=2,)
AZOO=dict(lion=4,zebra=9,elephant=3,tiger=7,)

class Inc(GuyCompo):

    def __init__(self,v):
        self.data.v=v 
        super().__init__()
    
    def build(self):
        return HBox(
            Button("-",onclick=self.bind.add(-1) ),         #<- bind GuyCompo event
            Text(self.data.v,style="text-align:center"),
            Button("+",onclick=self.bind.add(1) ),          #<- bind GuyCompo event
        )

    def add(self,v):
        self.data.v+=v



class Multi(GuyCompo):

    def __init__(self,dico: dict):
        self.data.dico=dico
        super().__init__()

    def build(self):
        d=VBox(style="padding:10px")
        for k,v in self.dataBind.dico.items():
            d.add( HBox( Text(k), Inc(v) ) )
        return d


class MyInput(GuyCompo):

    def __init__(self,txt):
        self.data.v=txt
        super().__init__()

    def build(self):
        return Input(type="text",value=self.data.v,onchange=self.bind.onchange("this.value"))

    def onchange(self,txt):
        self.data.v=txt



class JustGuy(GuyCompo):
    """ great version """
    size=(500,400)

    def __init__(self):
        self.data.selected={}
        self.data.text="hello1"
        self.data.text2="hello2"
        self.data.v=12
        self.data.tabSelected=1
        self.data.message=None
        super().__init__()

    def build(self):
        v= VBox(
            Inc(self.dataBind.v),
            Text(self.data.v),
            HBox(
                Text("name:"),
                # MyInput(self.data.text),
                MyInput(self.dataBind.text),                #<-- bind data
                Text(self.data.text)
            ),
            HBox(
                Text("surname:"),
                # MyInput(self.data.text),
                MyInput(self.dataBind.text2),                #<-- bind data
                Text(self.data.text2)
            ),
            HBox(
                Text("t1"),
                Button('b1',onclick="self.clickme('1')"),   #<-- classic guy call
                Button('b2',onclick='self.clickme("2")'),   #<-- classic guy call
            ),
            HBox(
                Text("Count animals",style="color:red"),
                Button('No!',onclick=self.bind.setMulti()),                         #<- bind GuyCompo event
                Button('In your house',onclick=self.bind.setMulti(1)),                         #<- bind GuyCompo event
                Button('In the zoo',onclick=self.bind.setMulti(2)),                              #<- bind GuyCompo event
            ),
            Multi(self.data.selected)                   #<-- bind data
        )
        if self.data.v>0:
            h=HBox()
            for i in range(self.data.v):
                h.add( Text("T%s"%(i+1)) )
            v.add( Box(h) )
        #=== tab
        t=MyTabs( self.dataBind.tabSelected ,["bonjour","bonsoir","hello"])
        v.add( t )
        v.add( Box( Text("content %s" % t.data.selected) ))
        #===
        if self.data.message:
            v.add( ModalMessage(self.dataBind.message) )
        return v

    def clickme(self,n):
        self.data.message="b%s clicked"%n
        self.data.text+="!"
        return self.update() #update manually !

    def setMulti(self,n=None):
        if n==1:
            self.data.selected=AHOUSE
        elif n==2:
            self.data.selected=AZOO
        else:
            self.data.selected={}


class MyTabs(GuyCompo):
    def __init__(self,selected:int,tabs:list):
        self.data.selected=selected
        self.data.tabs=tabs
        super().__init__()

    def build(self):
        o = Tabs()
        for idx,t in enumerate(self.data.tabs):
            o.addTab( idx+1==self.data.selected, t, onclick=self.bind.select(idx+1) ) 
        return o

    def select(self,idx):
        self.data.selected=idx

class ModalMessage(GuyCompo):
    def __init__(self,content):
        self.data.content=content
        super().__init__()

    def build(self):
        if self.data.content:
            o = Div(klass="modal is-active")
            o.add( Div(klass="modal-background",onclick=self.bind.close()) )
            o.add( Div( Box(self.data.content),klass="modal-content") )
            return o

    def close(self):
        self.data.content=None


if __name__=="__main__":
    # d=dict(a=2)
    # dd=DictReactiveProp(d)
    # dd["b"]=1
    # dd["a"]+=2
    # assert d=={'a': 4, 'b': 1}
    # print( render( dd["a"]) )
    # print( render( 4 ) )

    app=JustGuy()
    # app=MyTabs()
    # app=ModalMessage("Hello World")
    # app=Inc(0)
    # app=Multi(dict(name=12))
    app.run()
