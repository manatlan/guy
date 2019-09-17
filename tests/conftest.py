import pytest

# @pytest.fixture(params=["run","runCef","server"])
@pytest.fixture(params=["run","runCef"])
# @pytest.fixture(params=["run"])
# @pytest.fixture(params=["server"])
# @pytest.fixture(params=["runCef"])
def runner(request):
    def _( ga ):
        if request.param=="server":
            return getattr(ga,request.param)(port=10000)
        else:
            return getattr(ga,request.param)()

    return _