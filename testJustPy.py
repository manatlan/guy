#!/usr/bin/python3 -u
import guy,os,html

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
        attrs=['%s="%s"'%(k,html.escape(v)) for k,v in self.attrs.items()]
        return """<%(tag)s %(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag,
            attrs=" ".join(attrs),
            content=" ".join([i.render(False) if isinstance(i,GuyWidget) else str(i) for i in self.contents]),
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


class Link(Tag): 
    tag="a"
class Div(Tag):  pass
class HBox(Tag): pass
class VBox(Tag): pass
class Text(Tag):
    tag="span"
class Button(Tag):
    tag="button"


####################################################################################
class GuyWidget(guy.Guy):
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


class Inc(GuyWidget):

    def __init__(self,v):
        self.data=dict(v=v) # MUTABLE !!!
        super().__init__()
    
    def build(self):
        return HBox(
            Button("-1",onclick=self.bind.add(-1) ),         #<- bind guywidget event
            Text(self.data["v"],style="text-align:center"),
            Button("+1",onclick=self.bind.add(1) ),          #<- bind guywidget event
        )

    def add(self,v):
        self.data["v"]+=v


class Multi(GuyWidget):

    def __init__(self,dico):
        self.dico=dico
        super().__init__()

    def build(self):
        d=VBox(style="margin:10px")
        for k,v in self.dico.items():
            d.add( HBox( Text(k), Inc(v) ) )
        return d
        
AHOUSE=dict(cat=3,dog=2,)
AZOO=dict(lion=4,zebra=9,elephant=3,tiger=7,)

class JustPy(GuyWidget):
    """ great version """
    size=(400,200)
    data=dict(selected={}) # ! MUTABLE !!!

    def build(self):
        return VBox(
            HBox(
                Text("t1"),
                Button('b1',onclick="self.clickme('1')"),   #<-- classic guy call
                Button('b2',onclick='self.clickme("2")'),   #<-- classic guy call
            ),
            HBox(
                Text("Count animals",style="color:red"),
                Button('In your house',onclick=self.bind.setHouse()),                         #<- bind guywidget event
                Button('In the zoo',onclick=self.bind.setZoo()), #<- bind guywidget event
            ),
            Multi(self.data["selected"])
        )

    def clickme(self,n):
        print("click",n)

    def setHouse(self):
        self.data["selected"]=AHOUSE
    def setZoo(self):
        self.data["selected"]=AZOO

if __name__=="__main__":
    app=JustPy()
    # app=Inc(0)
    # app=Multi([1,2])
    app.run()
