#!/usr/bin/python
# -*- coding: utf-8 -*-
from guy import Guy
from datetime import datetime

class Simple(Guy):
    #~ size=FULLSCREEN
    size=(200,400)
    __doc__="""
    <style>body {margin:0px; padding:5px; border: 1px solid black}</style>
    <script>
    async function test() {
        var cpt=await guy.cfg.cpt || 0;
        var x=await self.getTimeStamp()
        document.querySelector("body").innerHTML += "<li>"+cpt+'/'+x+"</li>";
        guy.cfg.cpt=cpt+1
    }

    guy.init( test )
    </script>

    <img src="logo.png" width=42>
    <button onclick="test()">test</button>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    <hr/>
    """

    def getTimeStamp(self):
        return datetime.now()

if __name__ == "__main__":
    x=Simple()
    x.run()
