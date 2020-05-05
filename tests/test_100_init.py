from guy import Guy


def test_init(runner):
    class T(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            await self.append("C")
            await self.end()
        })
        </script>
        """
        def __init__(self):
            Guy.__init__(self)
            self.word=["A"]
        def init(self):
            self.append("B")
            
        def append(self,letter):
            self.word.append(letter)
        
        def end(self):
            self.exit(self.word)
    t=T()
    ll=runner(t)
    assert ll==list("ABC")


def test_init_async(runner):
    class T(Guy):
        __doc__="""
        <script>
        guy.init( async function() {
            await self.append("C")
            await self.end()
        })
        </script>
        """
        def __init__(self):
            Guy.__init__(self)
            self.word=["A"]

        async def init(self):
            self.append("B")

        def append(self,letter):
            self.word.append(letter)

        def end(self):
            self.exit(self.word)

    t=T()
    ll=runner(t)
    assert ll==list("ABC")
