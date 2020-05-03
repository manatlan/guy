from guy import Guy,http

@http(r"/item/(\d+)") 
def getItem(web,number):
  web.write( "item %s"%number )


def test_hook_with_classic_fetch(runner):
    class T(Guy):
        __doc__="""Hello
        <script>
        async function testHook() {
            var r=await window.fetch("/item/42")
            return await r.text()
        }
        </script>
        """
        async def init(self):
            self.retour =await self.js.testHook()
            self.exit()

    t=T()
    r=runner(t)
    assert r.retour == "item 42"



def test_hook_with_guy_fetch(runner):
    class T(Guy):
        __doc__="""Hello
        <script>
        async function testHook() {
            var r=await guy.fetch("/item/42") // not needed in that case (no cors trouble!)
            return await r.text()
        }
        </script>
        """
        async def init(self):
            self.retour =await self.js.testHook()
            self.exit()

    t=T()
    r=runner(t)
    assert r.retour == "item 42"

