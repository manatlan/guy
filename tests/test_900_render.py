from guy import Guy,http



def test_render(runner):
    class T(Guy):
        __doc__="""NOT USED"""

        async def init(self):
            self.retour =await self.js.end()

        def render(self,path):
            return """
            <script src="guy.js"></script>
            <script>
            function end() {
                if(self.render === undefined)   // render is not availaible as rpc js method !
                    self.end("ok")
            }
            </script>
            """

        def end(self,txt):
            self.ok=txt
            self.exit()
    
    t=T()
    r=runner(t)
    assert r.ok=="ok"

