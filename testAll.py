#!/usr/bin/python3 -u
import guy

"""
here, i will try to test a max of features in one file ...
(currently, it's the beginning)
"""

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
  
  function mark(t) {
    document.body.innerHTML+= `<li>${t}</li>`;
  }
  
  guy.on("evtMark", mark)
  </script>
  <button onclick="self.replay()">replay</button>
  """
    
  async def init(self):
      # call a simple js method at start
      await self.js.mark("py.init autocalled : ok")
    
      # call a js method which call a py method with param
      x=await self.js.callOk(42)
      await self.js.mark("callOk : %s " % ("ok" if x==84 else "ko"))

      # call a js method which call a unknonw py method
      try:
        x=await self.js.callKo()
      except guy.JSException:
        await self.js.mark("callKo : ok")

      # call a unknown js method
      try:
        x=await self.js.unknown()
      except guy.JSException:
        await self.js.mark("call unknown js : ok")

      # send a event to me
      await self.emitMe("evtMark","Try a perso event: ok")

      # send a event to all
      await self.emit("evtMark","Try a event to all: ok")

    
  def mulBy2(self,v):
    return v*2
  
  async def replay(self):
    await self.init()
  
if __name__ == "__main__": 
    App().serve()

