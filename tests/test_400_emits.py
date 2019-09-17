from guy import Guy

def test_emits(runner):
    class T(Guy):
        __doc__="""
        <script>
        var word="";

        guy.on( "hello", async function(letter) {
            word+=letter;
        })

        guy.on( "end", async function() {
            await self.endtest(word)
        })

        guy.init( async function() {
            guy.emitMe("hello","B")     // avoid socket, but it counts
            guy.emit("hello","C")       // emit all clients
            await self.makeEmits()       // generate server emits
        })

        guy.emitMe("hello","A")         // avoid socket, so can be run before init

        </script>
        """
        async def makeEmits(self):
            await self.emit("hello","D")      # emit all clients
            await self.emitMe("hello","E")         # emit ME only
            await self.emitMe("end")               # emit ME only and finnish the test
        def endtest(self,word):
            self.word=word
            self.exit()
    t=T()
    r=runner(t)
    assert r.word=="ABCDE"
