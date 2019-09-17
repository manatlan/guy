from guy import Guy


def test_doubleRun_sameInstance(runner):
    class T(Guy):
        __doc__="Hello"
        def init(self):
            self.ok=True
            self.exit()

    t=T()
    r=runner(t)
    assert r.ok
    t.ok=False
    r=runner(t)
    assert r.ok

