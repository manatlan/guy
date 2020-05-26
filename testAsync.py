#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,asyncio,time

class asyncTest(guy.Guy):
    __doc__="""
<style> body.wsguy {background:yellow} </style>

<script>
function rep(x) {
    document.getElementById("rep").innerHTML="<li>"+x+"</li>"+document.getElementById("rep").innerHTML;
}
</script>

<button onclick="self.doSyncQuick().then(rep)">sync quick</button>
<button onclick="self.doSyncLong().then(rep)">sync long (block ui)</button>
<button onclick="self.doASyncLong().then(rep)">async long</button>

<div id="rep"></div>
    """
    size=(200,200)

    def doSyncQuick(self):
        return "quick"

    def doSyncLong(self):           # run synchro (hangs the ui)
        time.sleep(3)
        return "long"

    async def doASyncLong(self):    # run asynchro !!! (it doesn't hang the UI !)
        await asyncio.sleep(3)
        return "async long"

if __name__=="__main__":
    app=asyncTest()
    app.run()
