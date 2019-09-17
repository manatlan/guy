from guy import Guy


def test_init(runner):
    class T(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            await self.append("C")
            guy.exit()
        })
        </script>
        """
        def __init__(self):
            Guy.__init__(self)
            self.word="A"
        def init(self):
            self.word+="B"
        def append(self,letter):
            self.word+=letter
        def __del__(self):
            self.word+="D"  # will be ignored (but perhaps in future ?!)
    t=T()
    r=runner(t)
    assert r.word=="ABC"

