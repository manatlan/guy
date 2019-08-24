
from guy import Guy

def test_exit_direct(runner):
    class TT(Guy):
        __doc__="""HELLO"""

    class T(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            var w=await self.win()
            self.parent.endtest()
        })
        </script>
        """
        def win(self):
            return TT()

        def endtest(self):
            self.ok=True
            self.exit()
    t=T()
    runner(t)
    assert t.ok

def test_wait_exit(runner):
    class TT(Guy):
        ok=True
        __doc__="""<script>self.exit()</script>"""


    class T(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            var w=await self.win()
            var ret=await w.run()
            self.endtest( ret.ok )
        })
        </script>
        """
        def win(self):
            return TT()
        def endtest(self,value):
            self.ok=value
            self.exit()
    t=T()
    runner(t)
    assert t.ok
