"""Tests for GET /activities endpoint"""


def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == 3
    for activity in expected_activities:
        assert activity in data


def test_get_activities_returns_correct_structure(client, reset_activities):
    """Test that activities have the correct data structure"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    # Assert
    assert response.status_code == 200
    for field in required_fields:
        assert field in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_participant_counts_match(client, reset_activities):
    """Test that participant counts are accurate"""
    # Arrange
    expected_participants = {
        "Chess Club": 2,
        "Programming Class": 2,
        "Gym Class": 2
    }
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, expected_count in expected_participants.items():
        actual_count = len(data[activity_name]["participants"])
        assert actual_count == expected_count
