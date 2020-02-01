#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy


class TestPyCallJs(guy.Guy):
    """
    <script>

    function myjsmethod(a,b) { 
        document.body.innerHTML+= `sync call (${a},${b})<br>`;
        return Math.random();
    }

    async function myLONGjsmethodAsync(a,b) { 
        document.body.innerHTML+= `async call long (${a},${b})...`;
        await new Promise(r => setTimeout(r, 2000));
        document.body.innerHTML+= `...ok<br>`;
        return Math.random();
    }

    async function myjsmethodAsync(a,b) { 
        document.body.innerHTML+= `async call (${a},${b})<br>`;
        return Math.random();
    }

    function myKAPUTTjsmethod() { 
        callInError(); // raise an exception on js side
    }

    async function myKAPUTTjsmethodAsync() { 
        callInError(); // raise an exception on js side
    }

    </script>
    <button onclick="self.test_ok()">call js ok</button>
    <button onclick="self.test_ok_async()">call async js ok</button>
    <button onclick="self.test_long_async()">call async long js ok</button>
    <button onclick="self.test_NF()">call js not found</button>
    <button onclick="self.test_ko()">call js ko</button>
    <button onclick="self.test_ko_async()">call async js ko</button>
    <button onclick="self.test_prompt()">test promt()</button>
    <br/>
    """
    size=(500, 300) # set the size of the client window

    async def test_prompt(self): 
        name = await self.js.prompt("Waht's your name ?")
        print("==========js returns=========>",name)
        return "ok prompt"

    async def test_ok(self): 
        r=await self.js.myjsmethod("Python World!",42)
        print("==========js returns=========>",r)
        return "ok sync"

    async def test_ok_async(self): 
        r=await self.js.myjsmethodAsync("Python World!",44)
        print("==========js returns=========>",r)
        return "ok async"

    async def test_long_async(self): 
        r=await self.js.myLONGjsmethodAsync("Python World!",45)
        print("==========js returns=========>",r)
        return "ok async"

    async def test_NF(self): 
        r=await self.js.myUNDECLAREDjsmethod()
        print("==========js returns=========>",r)
        return "nf"

    async def test_ko(self): 
        r=await self.js.myKAPUTTjsmethod()
        print("==========js returns=========>",r)
        return "ko"

    async def test_ko_async(self): 
        r=await self.js.myKAPUTTjsmethodAsync()
        print("==========js returns=========>",r)
        return "ko"

if __name__ == "__main__":
    TestPyCallJs().run(log=True)