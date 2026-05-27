import pytest

# All tests follow AAA: Arrange, Act, Assert

def test_get_activities(client):
    # Act
    res = client.get("/activities")
    # Assert
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data


def test_signup_new_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "test@student.edu"
    # Act
    res = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert res.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "dup@student.edu"
    # Act
    r1 = client.post(f"/activities/{activity}/signup?email={email}")
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 400


def test_signup_nonexistent_activity(client):
    # Act
    res = client.post("/activities/Nonexistent/signup?email=a@b.com")
    # Assert
    assert res.status_code == 404


def test_remove_participant(client):
    # Arrange
    activity = "Programming Class"
    email = "newp@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert res.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_remove_nonexistent_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "doesnotexist@x.com"
    # Act
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    # Assert
    assert res.status_code == 404
