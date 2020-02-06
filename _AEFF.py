#!/usr/bin/python3 -u
from guy import Guy,http

class Simplest(Guy):
    """
    <h1>Hello</h1>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    <button onclick="test()">test</button>
    <script>
    async function test() {
        r=await self.test()
        document.body.innerHTML+=r+"<br>";
    }
    </script>
    """
    def test(self):
        self.exit()
        # import time
        # return time.time()

@http(r"/myhookrunwindow") 
def myhook(web):
  return Simplest()

class T(Guy):
    __doc__="""Hello
    <a href="/myhookrunwindow">test</a>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    """

t=T()
r=t.run(log=True)
