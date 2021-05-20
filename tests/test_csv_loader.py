import requests
import requests_mock
from di_and_you.csv_loader import URL, load_csv_v1, load_csv_v2


def test_load_csv_v1(requests_mock, html_body):
    # this is about the only way you can test load_csv_v1
    # by using an external library to mock all of `requests`
    requests_mock.get(URL, text=html_body)

    data = load_csv_v1()

    assert 1 == len(data)
    elem = data[0]
    assert "AHS" == elem.name
    assert 0.16 == elem.cba_factor


def test_load_csv_v2(requests_mock, html_body):
    # you can do the same thing with v2
    requests_mock.get(URL, text=html_body)

    data = load_csv_v2(URL)

    assert 1 == len(data)
    elem = data[0]
    assert "AHS" == elem.name
    assert 0.16 == elem.cba_factor


def test_load_csv_v2_fine_grained_control(html_body):
    # but you can also get a little more fine grained control
    # using the same library to ensure that _other_ calls aren't made
    session = requests.Session()

    # control access to requests so that only the
    # single session and method work
    with requests_mock.Mocker():
        with requests_mock.Mocker(session=session) as mocker:
            mocker.get(URL, text=html_body)

            data = load_csv_v2(URL, session)

    assert 1 == len(data)
    elem = data[0]
    assert "AHS" == elem.name
    assert 0.16 == elem.cba_factor


def test_load_csv_v2_very_fine_grained_control(html_body):
    # or you can go off the rails and test completely different functionality
    # in this case we're replacing `requests.Session` completely
    # and testing how load_csv_v2 works with another session-like class
    class FakeResponse:
        def __init__(self, content: str):
            self.content = content

    class FakeSession:
        def __init__(self, content: str):
            self._response = FakeResponse(content)

        def get(self, *args, **kwargs):
            return self._response

    data = load_csv_v2(URL, FakeSession(html_body))

    assert 1 == len(data)
    elem = data[0]
    assert "AHS" == elem.name
    assert 0.16 == elem.cba_factor
