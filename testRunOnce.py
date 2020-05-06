#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from guy import Guy
from datetime import datetime

class Simple(Guy):
    size=(400,200)
    __doc__="""

    <script>
    function set() {
        localStorage["hello"]=new Date();
        init()
    }

    function init() {
        document.body.innerHTML += (localStorage["hello"] || "Empty");
    }

    </script>

    <button onclick="set()">set</button>

    <span style="color:yellow;background:red;padding:4;border:2px solid yellow;position:fixed;top:20px;right:20px;transform: rotate(10deg);">
If you try to run a second one<br/>
It will focus to this one !<br/>
(and keep storage !)
</span>
    """
    async def init(self):
        await self.js.init()

if __name__ == "__main__":
    x=Simple()
    x.run(one=True) # 11:21
