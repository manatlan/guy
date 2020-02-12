# import sys; sys.path.insert(0,"..")
from guy import Guy


def test_useStatic(runner):
    class UseStatic(Guy):
        classvar=45

        def __init__(self,v):
            self.instancevar=v
            Guy.__init__(self)

        def verif(self,a,b):
            self.somme = a+b
            self.exit()

    t=UseStatic(42)
    r=runner(t)
    assert r.somme == 87