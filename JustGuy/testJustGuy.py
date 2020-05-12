#!/usr/bin/python3 -u
from guycompo import GuyCompo
from tags import A,Body,Box,Button,Div,HBox,Input,Tabs,Tag,Text,Ul,VBox
from react import State

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
        for k,v in self.bind.dico.items():
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
            o.add( Div(klass="modal-close is-large",aria_label="close",onclick=self.bind.close()) )
            return o

    def close(self):
        self.data.content=None



class JustGuy(GuyCompo):
    """ great version """
    size=(500,400)

    def __init__(self,state):
        self.data.selected=state.selected
        self.data.text=state.text
        self.data.text2=state.text2
        self.data.v=state.v
        self.data.tabSelected=state.tabSelected
        self.data.message=state.message
        super().__init__()

    def build(self):
        v= VBox(
            Inc(self.bind.v),
            Text(self.data.v),
            HBox(
                Text("name:"),
                # MyInput(self.data.text),
                MyInput(self.bind.text),                #<-- bind data
                Text(self.data.text)
            ),
            HBox(
                Text("surname:"),
                # MyInput(self.data.text),
                MyInput(self.bind.text2),                #<-- bind data
                Text(self.data.text2)
            ),
            HBox(
                Text("t1"),
                Button('b1',onclick="self.clickme()"),   #<-- classic guy call (can only work if the class is the main instance !!!!) (doesn't work if nested)
                Button('b2',onclick=self.bind.clickme()),   #<-- classic guy call (but works even if it's nested!)
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
        t=MyTabs( self.bind.tabSelected ,["bonjour","bonsoir","hello"])
        v.add( t )
        v.add( Box( Text("content %s" % t.data.selected) ))
        #===
        if self.data.message:
            v.add( ModalMessage(self.bind.message) )
        return v

    def clickme(self):
        self.data.text+="!"
        return self.update() #update manually !

    def setMulti(self,n=None):
        if n==1:
            self.data.selected=AHOUSE
        elif n==2:
            self.data.selected=AZOO
        else:
            self.data.selected={}
            self.data.message="no more animals ;-)"



class Decor(GuyCompo):
    """ not a great object (with Tags building)
    But I leave it, like that, to make an example of including classic html/js (in guy's style)
    """
    def __init__(self,s):
        # self.data.content=content
        self.data.v=42
        self.data.openMenu=False
        self.state=s
        super().__init__()

    def build(self):
        kact = "is-active" if self.data.openMenu else ""

        return Body("""
<nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item">
      <b>MyApp</b>
    </a>

    <a role="button" class="navbar-burger burger %s" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" onclick="%s">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu %s">
    <div class="navbar-start">
      <a class="navbar-item">
        Home
      </a>

      <a class="navbar-item">
        Documentation
      </a>
    </div>

  </div>
</nav>


  <section class="section">
    <div class="container">""" % (kact,self.bind.switch(),kact),
      Inc(self.bind.v),
      JustGuy(self.state),
    """</div>
  </section>
""")

    def switch(self):
        self.data.openMenu=not self.data.openMenu


if __name__=="__main__":
    s=State(            # binded by justguy()
        selected={},
        text="hello1",
        text2="hello2",
        v=12,
        tabSelected=1,
        message=None,
    )


    app=Decor(s)
    app=JustGuy(s)
    # app=MyTabs(1,["hello","boy"])
    # app=ModalMessage("Hello World")
    # app=Inc(0)
    # app=Multi(dict(name=12))
    app.run()
