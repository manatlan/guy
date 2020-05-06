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
            ccfg=c
            scfg=self.cfg.value
            if self.cfg.unknown: scfg+=self.cfg.unknown

            self.exit(ccfg == scfg)
        
    t=T()
    ok=runner(t)
    if t.cfg._file and os.path.isfile(t.cfg._file): os.unlink(t.cfg._file)
    assert ok
