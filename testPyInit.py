#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,asyncio

class Init(guy.Guy):
    size=(200,200)
    __doc__="""
<script>
guy.on( "myevent", function(x) {
    document.querySelector("body").innerHTML+=x;
})
</script>"""

    def init(self):

        async def periodic():
            while True:
                await asyncio.sleep(0.5)
                await self.emit("myevent","X")

        asyncio.ensure_future(periodic())

if __name__ == "__main__":
    Init().run()
