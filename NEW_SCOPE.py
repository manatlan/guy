#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy,asyncio,time





class Index(guy.Guy):
    """
<a href="Search?q=yo">yo</a>

<button onclick="guy.emit('hello')">Emit</button>

<script>
guy.init( function() {
  guy.on("hello",function() {
    document.body.innerHTML+="X";
  })
})
</script>

    """
    size=(200,200)


class Search(guy.Guy):
    """
<script>
guy.init( function() {
  guy.on("hello",function() {
    document.body.innerHTML+="X";
  })
})
</script>
<h1>Search <<q>></h1>
<button onclick="self.jcall()">jcall</button>

    """
    size=(200,200)

    def __init__(self,q):
        self.q=q
        guy.Guy.__init__(self)
        
    async def jcall(self):
      await self.js.alert(32)
      
if __name__=="__main__":
    app=Index()
    app.serve(log=True)