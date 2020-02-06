
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
            self.ok=True
            self.exit()

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
    r=runner(t)
    assert r.ok

def test_redirect_exit(runner): # same concept as test_600_redirect.py ... but with better url
    db={}
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
            self.exit()
        })
        </script>
        2
        """

    t=W1()

    runner(t) # the returned instance is the main (t)
    assert True # but w2 has quit the main instance

