#!/usr/bin/python3 -u
from guy import Guy
import inspect 

class W1(Guy):
    __doc__="""
    <script>
    guy.init( async function() {
        if(document.location.href.indexOf("#W1")>=0) { // first call
            if(await self.step1())
                document.location.href="/W2"
        }
        else
            self.step3()
    })
    </script>
    1
    """
    def step1(self):
        return True
    def step3(self):
        self.ok=True
        self.exit()

class W2(Guy):
    __doc__="""
    <script>
    guy.init( async function() {
        if(await self.step2())
            document.location.href="/W1"
    })
    </script>
    2
    """
    def step2(self):
        return True

t=W1()
r=t.run(log=True)

