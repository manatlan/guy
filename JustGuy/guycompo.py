#!/usr/bin/python3 -u
import guy,os
from react import ReactiveProp,DictReactiveProp
from tags import Div

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
        """ to bind attribute or method !"""
        class Binder:
            def __getattr__(sself,name):
                if name in self._data.keys(): # bind a data attribut  -> return a ReactiveProp
                    o=self._data[name]
                    if isinstance(o,dict):
                        return DictReactiveProp(o)
                    elif isinstance(o,DictReactiveProp) or isinstance(o,ReactiveProp):
                        return o
                    else:
                        return ReactiveProp(self,name)
                elif name in self._routes.keys():   # bind a self.method    -> return a js/string for a guy's call in js side
                    def _(*args):
                        if args:
                            return "self.bindUpdate('%s','%s',%s)" % (self._id,name,",".join([str(i) for i in args]) ) #TODO: escaping here ! (and the render/str ?) json here !
                        else:
                            return "self.bindUpdate('%s','%s')" % (self._id,name)
                    return _
                else:
                    raise Exception("Unknown method/data '%s' in '%s'"%(name,self.__class__.__name__))
        return Binder()

    def render(self,path): # path is FAKED (by true/false) #TODO
        d=Div(id=self._id)
        d.add( self._caller( self.build ) )
        return d.render(path)

if __name__=="__main__":
    k=GuyCompo()
    k.data.x=42
    assert k.data.x==42
    assert isinstance(k.bind.x,ReactiveProp)
    assert k.bind.bindUpdate().startswith("self.bindUpdate(")
    assert k.bind.update().startswith("self.bindUpdate(")
