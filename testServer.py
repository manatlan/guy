#!/usr/bin/python
# -*- coding: utf-8 -*-
import guy,asyncio

class Server(guy.Guy):
    __doc__="""
<script>
guy.on( "tchat", function(x) {
    document.querySelector("body").innerHTML+="<li>"+x+"</li>";
})
</script>

<button onclick="guy.emitMe('tchat','emit to me')">Emit me</button>
<button onclick="guy.emit('tchat','emit to all')">Emit all</button>
<button onclick="guy.exit()">x</button>
"""


if __name__ == "__main__":
    Server().server()
