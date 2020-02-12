from guy import Guy,http
import os

def test_cfg(runner):
    class T(Guy):
        """
        <script>
        
        async function cadd() {
            guy.cfg.value = (await guy.cfg.value) +'(client)';
        }

        async function stop() {
            let c=await guy.cfg.value;
            let unknown = await guy.cfg.unknown
            if(unknown) c+=unknown
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
            if self.cfg.unknown: self.scfg+=self.cfg.unknown
            self.exit()
        
    t=T()
    r=runner(t)
    if t.cfg._file and os.path.isfile(t.cfg._file): os.unlink(t.cfg._file)
    assert r.ccfg == r.scfg == "(__init__)(init)(client)"
