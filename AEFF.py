#!/usr/bin/python3 -u
from guy import Guy

class T(Guy):
    __doc__="""
    <script>
    guy.init( async function() {
        await new Promise(r => setTimeout(r, 100)); // wait, to be sure that init() is called before step1()
        await self.append("C")
        guy.exit()
    })
    </script>
    """
    def __init__(self):
        Guy.__init__(self)
        self.word="A"

    def init(self):
        print("*****************************")
        self.append("B")
        
    def append(self,letter):
        print("_______________________APPEND",letter)
        self.word+=letter
    def __del__(self):
        self.word+="D"  # will be ignored (but perhaps in future ?!)
t=T()
r=t.run(log=True)
print(r.word)
assert r.word=="ABC"