#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy,asyncio,time





class Index(guy.Guy):
    """
<a href="Search?q=yo1">yo1</a>
<a href="Search?q=yo2">yo2</a>

<button onclick="self.jcall()">jcall vx</button>
<button onclick="guy.emit('hello','X')">Emit X</button>

<script>
guy.init( function() {
  guy.on("hello",function(x) {
    document.body.innerHTML+=x;
  })
})

function set(v) {
  guy.emitMe("hello",v)
}

</script>

    """
    size=(200,200)

    async def init(self):
        await self.js.set("ok")
        self.set("vx")
    
    def set(self,v):
        self.v=v
    
    async def jcall(self):
        await self.js.alert(self.v)


class Search(guy.Guy):
    """
<script>
guy.init( function() {
  guy.on("hello",function(x) {
    document.body.innerHTML+=x;
  })
})

function set(v) {
  guy.emitMe("hello",v)
}

</script>
<h1>Search <<q>></h1>
<button onclick="self.jcall()">jcall vs</button>
<button onclick="guy.emit('hello','S')">Emit S</button>
    """
    size=(200,200)

    def __init__(self,q):
        self.q=q
        guy.Guy.__init__(self)

    async def init(self):
        await self.js.set("ok")
        self.set("vs")
    
    def set(self,v):
        self.v=v
    
    async def jcall(self):
        await self.js.alert(self.v)


if __name__=="__main__":
    app=Index()
    app.serve(log=True)