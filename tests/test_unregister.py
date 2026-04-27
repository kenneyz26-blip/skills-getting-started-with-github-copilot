"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""


def test_unregister_removes_participant(client, reset_activities):
    """Test that DELETE unregister removes a participant"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_decreases_participant_count(client, reset_activities):
    """Test that unregister decreases the participant count"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])
    
    # Act
    client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    after_response = client.get("/activities")
    after_count = len(after_response.json()[activity_name]["participants"])
    
    # Assert
    assert after_count == before_count - 1


def test_unregister_removes_correct_participant(client, reset_activities):
    """Test that unregister removes the correct participant"""
    # Arrange
    removed_email = "michael@mergington.edu"
    remaining_email = "daniel@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    client.delete(
        f"/activities/{activity_name}/unregister?email={removed_email}"
    )
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert removed_email not in data[activity_name]["participants"]
    assert remaining_email in data[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_400(client, reset_activities):
    """Test that unregistering a non-existent participant returns 400"""
    # Arrange
    nonexistent_email = "nonexistent@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={nonexistent_email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"].lower()


def test_unregister_invalid_activity_returns_404(client, reset_activities):
    """Test that unregister from non-existent activity returns 404"""
    # Arrange
    email = "student@mergington.edu"
    invalid_activity = "Nonexistent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
