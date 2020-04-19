import pytest,time,asyncio

# @pytest.fixture(params=["run","runCef","serve"])
# @pytest.fixture(params=["run","runCef"])
@pytest.fixture(params=["run"])
# @pytest.fixture(params=["serve"])
# @pytest.fixture(params=["runCef"])
def runner(request):
    def _( ga, **kargs ):
        time.sleep(0.5) # leave the time to shutdown previous instance
        if request.param=="serve":
            return getattr(ga,request.param)(port=10000)
        else:
            return getattr(ga,request.param)(**kargs)

    return _

# @pytest.yield_fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()    