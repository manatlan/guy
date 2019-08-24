#!/usr/bin/python
# -*- coding: utf-8 -*-
import guy

class Fetch(guy.Guy):
    __doc__="""
<script>
guy.init( async function() {
    let url="https://manatlan.alwaysdata.net/?yo=12&jim=a"
    // var r=await fetch(url) //NOT POSSIBLE, COZ CORS
    var r=await guy.fetch(url)
    self.display( r.text())
})
</script>"""
    def display(self,m):
        print(m)

if __name__ == "__main__":
    Fetch().run()
