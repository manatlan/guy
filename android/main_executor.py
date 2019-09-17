#!/usr/bin/python
# -*- coding: utf-8 -*-
from guy import Guy
import tornado
import os

class Executor(Guy):
    #~ size=FULLSCREEN
    size=(200,400)
    __doc__="""
    <style>
    pre {border:1px solid red}
    button {font-size:2em}
    body {background: #FEE}
    </style>
    <script>
    async function test() {
        var x=await self.getTest()
        document.querySelector("#r").innerHTML = "<pre>"+x+"</pre>"+document.querySelector("#r").innerHTML;
    }
    </script>

    <button onclick="test()">test</button>
    <button onclick=' document.querySelector("#r").innerHTML ="" '>clear</button>
    <button style="float:right" onclick="self.exit()">X</button>
    <hr/>
    <div id="r"></div>
    """

    async def getTest(self):
        padLeft=lambda b: ("\n".join(["    "+i for i in b.splitlines()]))

        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch("https://manatlan.alwaysdata.net/executor", method="GET",validate_cert = False)
        try:
            c=response.body.decode().strip(" \t\n\r")
            code="def DYNAMIC():\n" + padLeft(c)
            exec( code , globals() )
            return DYNAMIC()
        except Exception as e:
            return "Error: %s" % e

if __name__ == "__main__":
    x=Executor()
    x.run()
