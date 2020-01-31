# import sys; sys.path.insert(0,"..")
from guy import Guy


def test_templateSubstitution(runner):
    class T(Guy):
        classvar=45
        __doc__="""
        <script>
        guy.init( async function() {
            await self.verif( <<classvar>>, <<instancevar>> )
        })
        </script>
        """
        def __init__(self,v):
            self.instancevar=v
            Guy.__init__(self)

        def verif(self,a,b):
            self.somme = a+b
            self.exit()
    t=T(42)
    r=runner(t)
    assert r.somme == 87