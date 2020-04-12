#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from guy import Guy
from datetime import datetime

class Simple(Guy):
    size=(200,400)
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
    """
    async def init(self):
        await self.js.init()

if __name__ == "__main__":
    x=Simple()
    x.runCef()
    # x.run(lockPort=22222) # 16:06:55
    # x.serve()
