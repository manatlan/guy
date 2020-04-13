import pytest,time

# @pytest.fixture(params=["run","runCef","serve"])
@pytest.fixture(params=["run","runCef"])
# @pytest.fixture(params=["run"])
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