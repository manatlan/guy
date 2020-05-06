from guy import Guy,http


class T(Guy):
    __doc__="""<script>
    async function storage(mode) {
        switch(mode) {
            case "get":
                return localStorage["var"]==42;
            case "set":
                localStorage["var"]=42;
                return true
            default:
                alert("mode='"+mode+"' ?!?")
        }
    
    }
    </script>"""
    size=(100,100)

    def __init__(self,mode):
        self.mode=mode
        super().__init__()

    async def init(self):
        ok =await self.js.storage(self.mode)
        self.exit(ok)

def test_no_lockPort(runner):
    t=T("get")
    ok=runner(t)
    assert not ok,"localStorage is already present ?!"

    t=T("set")
    ok=runner(t)
    assert ok,"setting localstorage not possible ?!"

    t=T("get")
    ok=runner(t)
    assert not ok,"win has memory ;-("

# CAN't WORK IN pytest, as is

# def test_lockPort(): # app mode only (broken with cef ... coz ioloop/pytests)
#     t=T("set")
#     ok=t.runCef(one=True)
#     assert ok==True

#     t=T("get")
#     ok=t.runCef(one=True)
#     assert ok==True                 # localStorage is persistent !
