#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy,asyncio,time

class Index(guy.Guy):
    """
<a href="Search?q=yo">yo</a>

<button onclick="self.exit()">Exit</button>

    """
    size=(200,200)


class Search(guy.Guy):
    """
<script>
</script>
<h1>Search <<q>></h1>
    """
    size=(200,200)

    def __init__(self,q):
        self.q=q
        guy.Guy.__init__(self)

if __name__=="__main__":
    app=Index()
    app.serve(log=False)
