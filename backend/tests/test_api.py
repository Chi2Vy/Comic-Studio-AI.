from fastapi.testclient import TestClient

from app.main import create_app


def test_health_and_catalog(tmp_path):
    client = TestClient(create_app(tmp_path / "studio.db"))
    assert client.get("/api/health").json()["ai_generation"] is False
    catalog = client.get("/api/catalog").json()
    assert len(catalog["styles"]) == 10
    assert len(catalog["moods"]) == 11
    assert len(catalog["modes"]) == 5


def test_projects_are_isolated_and_unverified(tmp_path):
    client = TestClient(create_app(tmp_path / "studio.db"))
    first = client.post("/api/projects", json={"title": "Truyện A"})
    second = client.post("/api/projects", json={"title": "Truyện B"})
    assert first.status_code == second.status_code == 201
    a, b = first.json(), second.json()
    assert a["rights_status"] == "unknown"
    assert len(client.get("/api/projects").json()) == 2

    ch = client.post(f"/api/projects/{a['id']}/chapters", json={
        "chapter_number": 1, "title": "Khởi đầu", "target_pages": 26
    })
    assert ch.status_code == 201
    assert client.post(f"/api/projects/{a['id']}/chapters", json={
        "chapter_number": 1, "title": "Trùng"
    }).status_code == 409

    character = client.post(f"/api/projects/{a['id']}/characters", json={"name": "An"})
    assert character.json()["model_status"] == "provisional"
    assert character.json()["approved_version"] is None

    beat = client.post(f"/api/projects/{a['id']}/beats", json={
        "beat_number": 1, "summary": "Gặp nhau", "source_locator": "Chương 1"
    })
    assert beat.json()["verification_level"] == "unverified"

    detail_a = client.get(f"/api/projects/{a['id']}").json()
    detail_b = client.get(f"/api/projects/{b['id']}").json()
    assert len(detail_a["chapters"]) == len(detail_a["characters"]) == len(detail_a["beats"]) == 1
    assert detail_b["chapters"] == detail_b["characters"] == detail_b["beats"] == []


def test_validation_and_not_found(tmp_path):
    client = TestClient(create_app(tmp_path / "studio.db"))
    assert client.get("/api/projects/not-found").status_code == 404
    assert client.post("/api/projects", json={"title": "X", "style_id": "invalid"}).status_code == 422
    assert client.post("/api/projects", json={"title": ""}).status_code == 422
    assert client.post("/api/projects/none/beats", json={"beat_number": 1, "summary": "A"}).status_code == 404
