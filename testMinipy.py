#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from guy import Guy,FULLSCREEN
import asyncio,datetime

class Minipy(Guy):
    size=(300,20)
    txt=" 3 * '#' "
    __doc__="""
<style>
div#back form {display:inline}
</style>
<script>
async function test(txt) {
    document.body.innerHTML += await self.post( txt )
}
</script>
<div id='back'>
    <h3>minipy</h3>
    <form onsubmit="test(this.txt.value); return false">
        <input id='n' name="txt" value="<<txt>>" onfocus="var val=this.value; this.value=''; this.value= val;" />
        <button> run </button>
    </form>
    <button onclick="self.exit()">exit</button>
</div>
<script>
document.querySelector("#n").focus()
</script>
    """

    def post(self,txt):
        try:
           return exec(txt, globals(), locals())
        except Exception as e:
           return "error:%s"%e


if __name__ == "__main__":
    x=Minipy()
    x.run(log=True)
