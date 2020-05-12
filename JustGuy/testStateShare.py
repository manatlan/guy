#!/usr/bin/python3 -u
from guycompo import GuyCompo
from tags import A,Body,Box,Button,Div,HBox,Input,Tabs,Text,Ul,VBox
from react import State

####################################################################################
## here come the tests
####################################################################################

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



class App(GuyCompo):
    size=(300,100)
    def __init__(self):
        self.data.v=12
        super().__init__()

    def build(self):
        d=Box(style="padding:10px")
        d.add( Inc(self.bind.v) )
        d.add( self.data.v )
        return d


if __name__=="__main__":
    # s=State(            # binded by justguy()
    #     selected={},
    #     text="hello1",
    #     text2="hello2",
    #     v=12,
    #     tabSelected=1,
    #     message=None,
    # )


    app=App()
    app.run()
