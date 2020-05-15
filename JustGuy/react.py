#!/usr/bin/python3 -u

""" WILL BE DELETED SOON """


class ReactiveProp:
    def __init__(self,instance,attribut:str):
        self.instance=instance
        self.attribut=attribut
    def set(self,v):
        self.instance._data[self.attribut]=v
    def get(self):
        return self.instance._data[self.attribut]


class DictReactiveProp:
    def __init__(self,d:dict):
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


class State:
    def __init__(self,**defaults):
        self._data=defaults

    def __getattr__(self,attr:str):
        if attr in self._data.keys():
            return ReactiveProp(self,attr)
        raise AttributeError("'%s' object has no attribute '%s'"%(self.__class__.__name__,attr))


if __name__=="__main__":
    d=dict(a=2)
    dd=DictReactiveProp(d)
    dd["b"]=1
    dd["a"]+=2
    assert d=={'a': 4, 'b': 1}


    s=State(cpt=6)
    assert isinstance(s.cpt,ReactiveProp)
    assert s.cpt.get() == 6
    assert s._data["cpt"]==6
    s.cpt.set(7)
    assert s.cpt.get() == 7
    assert s._data["cpt"]==7
    #~ print(s.xxx)