#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,asyncio

class progress(guy.Guy):    # name the class as the web/<class_name>.html
    __doc__="""
<style>
body {background: #EEE}
.pb {
    border:1px solid black;
    background:white;
}
.pb div {
    background:blue;
    height:20%;
    width:0px;
}
</style>

<button onclick="run(this,'p1',0.1)">Go</button>
<div class="pb" id="p1"><div></div></div>

<button onclick="run(this,'p2',0.02)">Go</button>
<div class="pb" id="p2"><div></div></div>

<script>
    function run(b,pb,speed) {
        b.disabled=true;
        self.doTheJob(pb,speed).then( m=>{
            b.disabled=false;
            console.log(m);
        })
    }
    guy.on("percent", function( pb,percent ) {
        document.querySelector("#"+pb+" div").style.width=percent+"%";
    })
</script>
    """
    async def doTheJob(self,pb,speed):
        for i in range(101):
            await asyncio.sleep(speed)    # simulate the job
            await self.emitMe("percent",pb,i)
        return "Job Done %s!" % pb


if __name__=="__main__":
    d=progress()
    d.serve()
