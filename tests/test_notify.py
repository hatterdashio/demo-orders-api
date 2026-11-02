from api import notify


class FakeResponse:
    status_code = 200

    def raise_for_status(self):
        pass


def test_notify_shipped_signs_the_request(monkeypatch):
    sent = {}

    def fake_post(url, data, headers, timeout, verify):
        sent.update(data=data, headers=headers)
        return FakeResponse()

    monkeypatch.setenv("CARRIER_SECRET", "not-a-real-secret")
    monkeypatch.setattr(notify.requests, "post", fake_post)

    assert notify.notify_shipped(7, "TRACK-1") == "sent"
    assert sent["headers"]["X-Signature"] == notify.signature(sent["data"])
