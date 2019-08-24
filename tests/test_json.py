
import guy
import asyncio
from datetime import date, datetime

def test_json():
    def test(j, testType=None):
        def testSUS(obj, testType=None):
            s = guy.jDumps(obj)
            nobj = guy.jLoads(s)
            assert type(nobj) == testType

        testSUS(dict(v=j), dict)
        testSUS([j, dict(a=[j])], list)
        testSUS(j, testType)

    class Ob:
        def __init__(self):
            self.name = "koko"

    test(datetime.now(), datetime)
    test(date(1983, 5, 20), datetime)
    test(b"kkk", str)
    test("kkk", str)
    test(42, int)
    test(4.2, float)
    test(None, type(None))
    test(Ob(), dict)
    test(datetime.now() - datetime.now(), str)
