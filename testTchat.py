#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,asyncio

class Tchat(guy.Guy):
    __doc__="""
<form onsubmit="guy.emit( 'evt-send-txt', this.txt.value ); return false">
    <input id="txt" value=""/>
    <input type="submit" value="ok"/>
</form>    

<script>
guy.on( "evt-send-txt", function(txt) { 
    document.body.innerHTML+=`<li>${txt}</li>`; 
    document.querySelector("#txt").focus();
})
</script>

<span style="color:yellow;background:red;padding:4;border:2px solid yellow;position:fixed;top:20px;right:20px;transform: rotate(10deg);">
Open a second tab (better: from another computer)<br/>
to see this simple tchat on ;-)
</span>"""


if __name__ == "__main__":
    Tchat().serve()
