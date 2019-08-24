#!/usr/bin/python
# -*- coding: utf-8 -*-
import guy,asyncio

class Init(guy.Guy):
    size=(200,200)
    __doc__="""
<script>
guy.init( function() {
    setInterval( function(){ self.display('X')}, 1000)
})
</script>"""

    def display(self,x):
        print(x)

if __name__ == "__main__":
    Init().run()
