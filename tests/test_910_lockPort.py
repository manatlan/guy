from guy import Guy,http


class T(Guy):
    __doc__="""<script>
    async function storage(mode) {
        switch(mode) {
            case "get":
                alert(localStorage["var"])
                return localStorage["var"]==42;
            case "set":
                alert(localStorage["var"])
                localStorage["var"]=42;
                return true
        }
    
    }
    </script>"""
    size=(100,100)

    def __init__(self,mode):
        self.mode=mode
        Guy.__init__(self)

    async def init(self):
        self.ok =await self.js.storage(self.mode)
        self.exit()

def test_no_lockPort(runner):
    t=T("get")
    r=runner(t)
    assert r.ok==False

    t=T("set")
    r=runner(t)
    assert r.ok==True

    t=T("get")
    r=runner(t)
    assert r.ok==False

## can't work as expected
## btw, it works manually
## but not in tnr ;-(

# def test_lockPort(runner):
#     lockPort=28417

#     t=T("get")
#     r=runner(t,lockPort=lockPort)
#     assert r.ok==False

#     t=T("set")
#     r=runner(t,lockPort=lockPort)
#     assert r.ok==True

#     t=T("get")
#     r=runner(t,lockPort=lockPort)
#     assert r.ok==True
