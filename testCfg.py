#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,asyncio,datetime

class Cfg(guy.Guy):
    size=(300,20)
    __doc__="""
<script>
guy.init( async function(){
    document.body.innerHTML += await guy.cfg.kiki;
})
</script>
    """
    def __init__(self,d):
        guy.Guy.__init__(self)
        self.d=d
    def init(self):
        self.cfg.kiki=self.d


if __name__ == "__main__":
    Cfg( datetime.datetime.now() ).run()


