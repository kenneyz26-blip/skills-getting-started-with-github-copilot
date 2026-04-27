"""Tests for POST /activities/{activity_name}/signup endpoint"""


def test_signup_for_activity_success(client, reset_activities):
    """Test successful signup for an activity"""
    # Arrange
    new_email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert new_email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_activity(client, reset_activities):
    """Test that signup actually adds the participant to the activity"""
    # Arrange
    new_email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    original_response = client.get("/activities")
    original_count = len(original_response.json()[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup?email={new_email}")
    updated_response = client.get("/activities")
    updated_data = updated_response.json()
    
    # Assert
    assert new_email in updated_data[activity_name]["participants"]
    assert len(updated_data[activity_name]["participants"]) == original_count + 1


def test_signup_duplicate_email_returns_400(client, reset_activities):
    """Test that duplicate signup returns 400 error"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_invalid_activity_returns_404(client, reset_activities):
    """Test that signup to non-existent activity returns 404"""
    # Arrange
    email = "student@mergington.edu"
    invalid_activity = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_updates_participant_count_correctly(client, reset_activities):
    """Test that signup updates the participant count correctly"""
    # Arrange
    new_email = "newstudent@mergington.edu"
    activity_name = "Programming Class"
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup?email={new_email}")
    after_response = client.get("/activities")
    after_count = len(after_response.json()[activity_name]["participants"])
    
    # Assert
    assert after_count == before_count + 1
