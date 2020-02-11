#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy


class TestPyCallJs(guy.Guy):
    """
    <script>

    function myjsmethod(a,b) { 
        document.body.innerHTML+= `sync call (${a},${b})<br>`;
    }

    class Jo {
        constructor() {}
        add(a,b) {
            alert(a+b)
        }
    }
    jo=new Jo()

    </script>
    <button onclick="self.test_ok()">call js ok</button>
    <br/>
    """
    size=(500, 300) # set the size of the client window

    async def test_ok(self): 
        r=await self.js["jo.add"]("Python World!",42)
        print("==========js returns=========>",r)
        return "ok sync"

if __name__ == "__main__":
    TestPyCallJs().run(log=True)