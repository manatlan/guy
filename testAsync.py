#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,asyncio,time

class asyncTest(guy.Guy):    # name the class as the web/<class_name>.html
    __doc__="""
<script>
function rep(x) {
    document.getElementById("rep").innerHTML="<li>"+x+"</li>"+document.getElementById("rep").innerHTML;
}
</script>

<button onclick="self.doSyncQuick().then(rep)">s quick</button>
<button onclick="self.doSyncLong().then(rep)">s long</button>
<button onclick="self.doASyncLong().then(rep)">as long</button>

<div id="rep"></div>
    """

    def doSyncQuick(self):
        return "quick"

    def doSyncLong(self):           # run synchro (hangs the ui)
        time.sleep(2)
        return "long"

    async def doASyncLong(self):    # run asynchro !!! (it doesn't hang the UI !)
        await asyncio.sleep(2)
        return "async long"

if __name__=="__main__":
    d=asyncTest()
    d.run()
