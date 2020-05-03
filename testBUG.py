#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy,asyncio

class BUG(guy.Guy):    # name the class as the web/<class_name>.html
    """
    <button onclick="self.callEvent()">Test evt</button>
    <button onclick="self.callJS()">Test call js</button>
    <button onclick="self.exit();window.close()">X</button>
    <div id="r">0</div>
    <a href="/Other">other</a>

    <script>
        function callInc() {
            let r=document.querySelector("#r");
            r.innerHTML=parseInt(r.innerHTML)+1
        }

        guy.on("evtInc", callInc)
    </script>
    """

    async def init(self):
        await self.js.alert("ok")

    async def callEvent(self):
        await self.emitMe("evtInc")

    async def callJS(self):
        await self.js.callInc()

class Other(guy.Guy):    # name the class as the web/<class_name>.html
    """
    <a href="/">back</a>
    """



if __name__=="__main__":
    d=BUG()
    d.serve(log=True)
