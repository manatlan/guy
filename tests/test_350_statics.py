# import sys; sys.path.insert(0,"..")
from guy import Guy


def test_useStatic(runner):
    class UseStatic(Guy):
        classvar=45

        def __init__(self,v):
            self.instancevar=v
            Guy.__init__(self)

        def verif(self,a,b):
            self.exit(a+b)

    t=UseStatic(42)
    total=runner(t)
    assert total == 87