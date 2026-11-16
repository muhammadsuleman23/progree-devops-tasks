import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
import main  # noqa: E402


class FakeRedis:
    def __init__(self):
        self.count = 0

    def incr(self, key):
        self.count += 1
        return self.count

    def ping(self):
        return True


def test_index_counts_hits(monkeypatch):
    monkeypatch.setattr(main, "cache", FakeRedis())
    client = main.app.test_client()
    assert client.get("/").get_json()["hits"] == 1
    assert client.get("/").get_json()["hits"] == 2


def test_health_ok(monkeypatch):
    monkeypatch.setattr(main, "cache", FakeRedis())
    response = main.app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
