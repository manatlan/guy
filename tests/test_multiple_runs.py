from guy import Guy


def test_doubleRun_sameInstance(runner):
    class T(Guy):
        __doc__="Hello"
        def init(self):
            self.ok=True
            self.exit()

    t=T()
    runner(t)
    assert t.ok
    t.ok=False
    runner(t)
    assert t.ok

