import pytest
from ninja.testing import TestClient

@pytest.mark.django_db
def test_successful_claim(client, user, jwt_token):
    task = TaskFactory(status=TaskStatus.UNASSIGNED.value, owner=None)
    response = client.patch(f"/api/tasks/{task.id}/claim", headers=jwt_token)
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.status == TaskStatus.IN_PROGRESS.value
    assert task.owner == user
