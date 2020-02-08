#!/usr/bin/python3 -u
from guy import Guy,http

class Simplest(Guy):
    """
    <h1>Hello <<msg>></h1>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    <button onclick="test()">test</button>
    <script>
    function init() {
        document.body.innerHTML+="init<br>";
    }

    async function test() {
        r=await self.test()
        document.body.innerHTML+=r+"<br>";
    }
    </script>
    """
    def __init__(self,txt):
        Guy.__init__(self)
        self.msg=txt

    async def init(self):
        await self.js.init()

    def test(self):
        import time
        return time.time()

@http(r"/myhookrunwindow/(.+)")
def myhook(web,msg):
    return Simplest(msg)

class T(Guy):
    """Hello
    <a href="/myhookrunwindow/HookWindow">test</a>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    """

t=T()
r=t.run(log=True)
