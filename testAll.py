#!/usr/bin/python3 -u
import guy

"""
here, i will try to test a max of features in one test/file ...
(currently, it's the beginning)
"""

@guy.http(r"/item/(\d+)") 
def getItem(web,number):
    web.write( "item %s"%number )
  

class App(guy.Guy):
    """
    <script>
    async function callOk(v) {
      return await self.mulBy2(v)
    }
    
    async function callKo() {
      await self.unknowMethod()
      return "ok"
    }
    
    var MARKS=[]
    function mark(t) {
      MARKS.push(t)
      document.body.innerHTML+= `<li>${t}</li>`;
    }
    
    guy.on("evtMark", mark)

    
    async function changeConfig() {
      let v = await guy.cfg.cptClient || 0;
      guy.cfg.cptClient = v+1;
      mark("js: guy.cfg set/get : ok")
    }

    function testFetch() {
      window.fetch("/item/42")
        .then( x=>{return x.text()})
        .then( x=>{ 
          if(x=="item 42")
            mark("windows fetch/hook : ok")
        })
    }

    function testGFetch() {
      guy.fetch("/item/42")
        .then( x=>{return x.text()})
        .then( x=>{ 
          if(x=="item 42")
            mark("guy fetch/hook : ok")
        })
    }

    function testSubVar() {
      return "<<myVar>>";
    }
    
    async function finnish() {
      self.exit( MARKS )
    }

    
    </script>
    <button onclick="self.init()">replay</button>
    """
    myVar="ThisIsAVar"
    
    
    async def init(self):
        # call a simple js method at start
        await self.js.mark("py.init autocalled : ok")
      
        # test that's the var substitution mechanism is working
        v=await self.js.testSubVar()
        await self.js.mark("var substituion : %s" % (v==App.myVar and "ok" or "ko"))

        # test the call of a real js window.method
        v=await self.js.parseInt("42")
        await self.js.mark("call a real js method : %s" % (v==42 and "ok" or "ko"))
      
        # call a js method which call a py method with param
        x=await self.js.callOk(42)
        await self.js.mark("callOk : %s " % ("ok" if x==84 else "ko"))

        # call a js method which call a unknonw py method
        try:
          x=await self.js.callKo()
          await self.js.mark("callKo : ko")
        except guy.JSException:
          await self.js.mark("callKo : ok")

        # call a unknown js method
        try:
          x=await self.js.unknown()
          await self.js.mark("call unknown js : ko")
        except guy.JSException:
          await self.js.mark("call unknown js : ok")

        # send a event to me
        await self.emitMe("evtMark","Try a perso event: ok")

        # send a event to all
        await self.emit("evtMark","Try a event to all: ok")

        # change config client side
        await self.js.changeConfig()
        
        # change config server side
        v=self.cfg.cptServer or 0
        self.cfg.cptServer = v+1
        await self.emit("evtMark","py: self.cfg set/get : ok")
        
        # test the http hook with js/window.fetch
        await self.js.testFetch()
        
        # test the http hook with js/guy.fetch (the proxy)
        await self.js.testGFetch()

        await self.js.finnish()
      
    def mulBy2(self,v):
        return v*2
        
        
if __name__ == "__main__": 
    app=App()
    ll=app.run(log=True)
    assert ll==['py.init autocalled : ok', 'var substituion : ok', 'call a real js method : ok', 'callOk : ok ', 'callKo : ok', 'call unknown js : ok', 'Try a perso event: ok', 'Try a event to all: ok', 'js: guy.cfg set/get : ok', 'py: self.cfg set/get : ok', 'windows fetch/hook : ok', 'guy fetch/hook : ok']
