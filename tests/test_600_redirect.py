
from guy import Guy

def test_redirect(runner):
    class W1(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            if(document.location.href.indexOf("#W1")>=0) { // first call
                if(await self.step1())
                    document.location.href="/W2?param=42"
            }
            else
                self.step3()
        })
        </script>
        1
        """
        def step1(self):
            return True
        def step3(self):
            self.exit(True)

    class W2(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            if(await self.step2())
                document.location.href="/W1"
        })
        </script>
        2
        """
        def __init__(self,param):
            Guy.__init__(self)
            assert param == "42"
        def step2(self):
            return True

    t=W1()
    ok=runner(t)
    assert ok

def test_redirect_exit(runner): # same concept as test_600_redirect.py ... but with better url

    class W1(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            document.location.href="/W2?param=42"   // the param is ignored
        })
        </script>
        1
        """

    class W2(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            self.end()
        })
        </script>
        2
        """
        def end(self):
            assert self.parent
            self.exit(True)


    t=W1()

    ok=runner(t) # it's W2 which exit
    assert ok

