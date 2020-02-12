from guy import Guy,http

#TODO: manage config.json (remove before runned, and delete after)

def test_cfg(runner):
    class T(Guy):
        """
        <script>
        
        async function cadd() {
            guy.cfg.value = (await guy.cfg.value) +'(client)';
        }

        async function stop() {
            let c=await guy.cfg.value;
            self.stop(c)
        }

        </script>

        """
        def __init__(self):
            Guy.__init__(self)
            self.cfg.value = "(__init__)"

        async def init(self):
            self.cfg.value += "(init)"
            await self.js.cadd()
            await self.js.stop()

        def stop(self,c):
            self.ccfg=c
            self.scfg=self.cfg.value
            self.exit()
        
    t=T()
    r=runner(t)
    assert r.ccfg == r.scfg == "(__init__)(init)(client)"

