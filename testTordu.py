#!/usr/bin/python
# -*- coding: utf-8 -*-
from guy import Guy
from datetime import datetime

class Simplest(Guy):
    size=(200,200)
    __doc__="""
    <h1>Hello</h1>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    """


class Tordu(Guy):
    size=(200,400)
    __doc__="""
    <style>body {margin:0px; padding:5px; border: 1px solid black}</style>
    <script>
    async function testInstance() {
        var x=await self.testInstance()
    }
    async function testJsReturn() {
        var x=await self.testJsReturn()
    }

    </script>

    <button onclick="testInstance()">Run another instance</button>
    <button onclick="testJsReturn()">testJsReturn</button>
    <button onclick="self.testOpen()">testOpen</button>
    <button style="float:right;font-size:2em" onclick="guy.exit()">X</button>
    <hr/>
    """

    def testInstance(self):
        t=Simplest()
        t.run()

    async def testJsReturn(self):
        return dict( script="guy.exit()" ) #it's evil!

    def testOpen(self):
        return Simplest()

if __name__ == "__main__":
    x=Tordu()
    x.run()
