# this import sucks, `conn` is created on import,
# meaning there's an empty file hanging out on my filesystem
from di_and_you import db
from di_and_you.db import FactorDbV1, FactorDbV2
from di_and_you.csv_loader import URL, Row, load_csv_v2


def test_factor_db_v1(requests_mock, monkeypatch, test_conn, html_body):  # noqa
    # need to mock the low level call somehow, either
    # by doing the same request mocks or by monkeypatching the
    # load_csv_v1 attr of db
    requests_mock.get(URL, text=html_body)

    # need to replace the conn with out test conn to ensure an
    # in memory db
    monkeypatch.setattr(db, "conn", test_conn)

    test_db = FactorDbV1()
    test_db.load_db()

    assert 1 == test_db.count()


def test_factor_db_v2(test_conn):
    # can substitute your own test data
    test_data = [Row("foo", "bar", "baz", 0.15)]
    test_db = FactorDbV2(test_conn)
    test_db.load_db(test_data)
    assert 1 == test_db.count()


def test_factor_db_v2_e2e(requests_mock, test_conn, html_body):
    # or do a mock e2e test like test_factor_db_v1
    # but the setup is much easier, here than above
    # and doesn't break when you change package structure
    requests_mock.get(URL, text=html_body)
    test_data = load_csv_v2(URL)
    test_db = FactorDbV2(test_conn)
    test_db.load_db(test_data)
    assert 1 == test_db.count()
