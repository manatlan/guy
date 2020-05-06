from guy import Guy


def test_doubleRun_sameInstance(runner):
    class T(Guy):
        __doc__="Hello"
        def init(self):
            self.exit(True)

    t=T()
    ok=runner(t)
    assert ok
    ok=runner(t)
    assert ok

