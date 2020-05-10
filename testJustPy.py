#!/usr/bin/python3 -u
import guy,os,html

""" A lot Inspired by Vue syntax ! 

At the beginning, it was just a test to try to reproduce with "Guy", things like :
- justpy
- https://www.reddit.com/r/Python/comments/gfq5ik/i_wrote_a_new_ui_framework_inspired_by_flutter/
- flutter

But things going better and better ... without magical things
Helped by the vuejs ideas: it seems good in py side !
And so : it could clearly the future of "Guy Components" ;-)
"""

class GetterSetter:
    def __init__(self,instance,attribut):
        self.instance=instance
        self.attribut=attribut
    def set(self,v):
        self.instance._data[self.attribut]=v
    def get(self):
        return self.instance._data[self.attribut]


class DictGetterSetter:
    def __init__(self,d):
        self._data=d
    def __setitem__(self,k,v):
        g=GetterSetter(self,k)
        g.set(v)
    def __getitem__(self,k):
        g=GetterSetter(self,k)
        return g.get()
    def items(self):
        for k in self._data.keys():
            yield k,GetterSetter(self,k)


class Tag:
    tag="div" # default one
    def __init__(self,*contents,**attrs):
        self.tag=self.__class__.tag
        self.contents=list(contents)
        self.attrs=attrs
        self.attrs["class"]=self.__class__.__name__
    def add(self,o):
        self.contents.append(o)
    def __repr__(self):

        def render(c):
            if isinstance(c,GuyCompo):
                return c.render(False)
            # if isinstance(c,GetterSetter): #TODO: not needed ... check that ?!
            #     return c.get()
            else:
                return str(c)            

        attrs=['%s="%s"'%(k,html.escape( render(v) )) for k,v in self.attrs.items()]
        return """<%(tag)s %(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag,
            attrs=" ".join(attrs),
            content=" ".join([render(i) for i in self.contents]),
        )
    def render(self,full=False):
        if full:
            return """<script src="guy.js"></script>
<style>
html,body {width:100%%;height:100%%;}
body {margin:0px;background:buttonface;font-family: sans-serif;}
div.HBox {display: flex;flex-flow: row nowrap;}
div.VBox {display: flex;flex-flow: column nowrap;}
div.HBox > *,div.VBox > * {flex: 1 1 50%%;}
</style> <body>%s</body>""" % self
        else:
            return str(self)


class Input(Tag): 
    tag="input"
class Link(Tag): 
    tag="a"
class Div(Tag):  pass
class HBox(Tag): pass
class VBox(Tag): pass
class Text(Tag):
    tag="span"
class Button(Tag):
    tag="button"


class GuyCompo(guy.Guy):
    
    @property
    def data(self): # MUTABLE !
        if not hasattr(self,"_data"): self._data={}
        class DataBinder:
            def __setattr__(zelf,k,v):
                o=self._data.get(k)
                if o and isinstance(o,GetterSetter):
                    o.set(v)
                else:
                    self._data[k]=v
            def __getattr__(zelf,k):
                o=self._data[k]
                if isinstance(o,GetterSetter):
                    return o.get()
                else:
                    return o
        return DataBinder()

    @property
    def dataBind(self):
        class Binder:
            def __getattr__(sself,attribut):
                assert attribut in self._data.keys(),"Unknown attribut '%s'"%attribut
                o=self._data[attribut]
                if isinstance(o,dict):
                    return DictGetterSetter(o)
                elif isinstance(o,DictGetterSetter):
                    return o
                else:
                    return GetterSetter(self,attribut)
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
            # and update all the content
            return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (
                id, self._caller( zelf.build ).render(False)
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
                        return "self.bindUpdate('%s','%s',%s)" % (self._id,method,",".join([str(i) for i in args]) )
                    else:
                        return "self.bindUpdate('%s','%s')" % (self._id,method)
                return _
        return Binder()

    def render(self,path): # path is FAKED (by true/false) #TODO
        d=Div(id=self._id)
        d.add( self._caller( self.build ) )
        return d.render(path)
####################################################################################


class Inc(GuyCompo):

    def __init__(self,v):
        self.data.v=v 
        super().__init__()
    
    def build(self):
        return HBox(
            Button("-1",onclick=self.bind.add(-1) ),         #<- bind GuyCompo event
            Text(self.data.v,style="text-align:center"),
            Button("+1",onclick=self.bind.add(1) ),          #<- bind GuyCompo event
        )

    def add(self,v):
        self.data.v+=v



class Multi(GuyCompo):

    def __init__(self,dico):
        self.data.dico=dico
        super().__init__()

    def build(self):
        d=VBox(style="margin:10px")
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


AHOUSE=dict(cat=3,dog=2,)
AZOO=dict(lion=4,zebra=9,elephant=3,tiger=7,)

class JustPy(GuyCompo):
    """ great version """
    size=(400,200)

    def __init__(self):
        self.data.selected={}
        self.data.text="hello"
        self.data.v=12
        super().__init__()

    def build(self):
        return VBox(
            Inc(self.dataBind.v),
            HBox(
                Text("name:"),
                # MyInput(self.data.text),
                MyInput(self.dataBind.text),                #<-- bind data
            ),
            HBox(
                Text("t1"),
                Button('b1',onclick="self.clickme('1')"),   #<-- classic guy call
                Button('b2',onclick='self.clickme("2")'),   #<-- classic guy call
            ),
            HBox(
                Text("Count animals",style="color:red"),
                Button('In your house',onclick=self.bind.setHouse()),                         #<- bind GuyCompo event
                Button('In the zoo',onclick=self.bind.setZoo()),                              #<- bind GuyCompo event
            ),
            Multi(self.dataBind.selected)                   #<-- bind data
        )

    def clickme(self,n):
        print("click",n)
        self.data.text+="!"

    def setHouse(self):
        self.data.selected=AHOUSE
    def setZoo(self):
        self.data.selected=AZOO

if __name__=="__main__":
    app=JustPy()
    # app=Inc(0)
    # app=Multi(dict(name=12))
    app.run()
