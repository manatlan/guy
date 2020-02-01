
from guy import Guy,JSException

def test_jscall(runner):
    class W1(Guy):
        __doc__="""
        <script>
        var ll=[];

        function adds(a,b) {
            ll.push(a)
            ll.push(b)
            return a+b
        }

        function makeAnError() {
            callInError(); // raise an exception on js side
        }

        async function ASyncAdds(a,b) {
            ll.push(a)
            ll.push(b)
            return a+b
        }

        guy.init( async function() {
            await new Promise(r => setTimeout(r, 100)); // wait, to be sure that init() is called before step1()
            await self.step1()
            await self.step2()
            self.stop( ll )
        })

        </script>
        """
        async def init(self):
            self.ll=[]
            self.ll.append( await self.js.adds("A","B") )

        async def step1(self):
            self.ll.append( await self.js.adds("C","D") )
            self.ll.append( await self.js.ASyncAdds("E","F") )

        async def step2(self):
            try:
                await self.js.UNKNOWNMETHOD("C","D")
            except JSException:
                self.ll.append("Unknown")
            try:
                await self.js.makeAnError()
            except JSException:
                self.ll.append("Error")

        def stop(self,jll):
            assert jll==['A', 'B', 'C', 'D', 'E', 'F']
            assert self.ll==['AB', 'CD', 'EF', 'Unknown', 'Error']
            self.ok=True
            self.exit()

    t=W1()
    r=runner(t)
    assert r.ok
