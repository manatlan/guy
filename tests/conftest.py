import pytest

@pytest.fixture(params=["run","runCef","server"])
# @pytest.fixture(params=["run","runCef"])
# @pytest.fixture(params=["run"])
# @pytest.fixture(params=["server"])
# @pytest.fixture(params=["runCef"])
def runner(request):
    def _( ga ):
        if request.param=="server":
            getattr(ga,request.param)(port=10000)
        else:
            getattr(ga,request.param)()

    return _