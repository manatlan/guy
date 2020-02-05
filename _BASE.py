#!/usr/bin/python3 -u
from guy import Guy
import inspect 

class T(Guy):
    __doc__="""
    <script>
    guy.init( async function() {
        await self.mappend("C")
        self.exit()
    })
    </script>
    """
    
    def __init__(self):
        Guy.__init__(self)
        self.word=""
        self.mappend("A")

    def init(self):
        self.mappend("B")
        
    def mappend(self,letter):
        print("_______________________APPEND",letter)
        self.word+=letter
        
        
t=T()
r=t.run(log=True)
assert r.word=="ABC"
