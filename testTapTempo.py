#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,datetime

class TapTempo(guy.Guy):
    __doc__="""
    <style>
    body {background: yellow}
    #tempo {font-size:3em}
    </style>
    <button style="float:right;font-size:2em" onclick="self.exit()">X</button>
    <script>
        function tap() {
            self.tap().then(x=>{document.querySelector('#tempo').innerHTML=x})
        }
        document.onclick=tap
    </script>
    <center>Tap Tempo!</center>
    <center id="tempo"></center>
    """
    size=(100,60)
    t=[]

    def tap(self):
        self.t.append( datetime.datetime.now() )
        ll=[ (j-i).microseconds for i, j in zip(self.t[:-1], self.t[1:]) ][-5:]
        if ll:
            return int(60000000*len(ll)/sum(ll))

if __name__ == "__main__":
    TapTempo().run()
