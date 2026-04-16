"""Tests for POST /activities/{activity_name}/signup endpoint"""


class TestSignupEndpoint:
    """Test suite for activity signup functionality"""
    
    def test_signup_adds_participant_to_activity(self, client):
        """
        Arrange: Select an activity with available spots
        Act: Sign up a new student
        Assert: Student is added to participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was actually added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_returns_success_message(self, client):
        """
        Arrange: Prepare signup request
        Act: Send signup request
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "student123@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_fails_for_nonexistent_activity(self, client):
        """
        Arrange: Prepare signup for non-existent activity
        Act: Attempt signup
        Assert: Returns 404 not found error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_fails_for_duplicate_registration(self, client):
        """
        Arrange: A student is already registered for an activity
        Act: Attempt to sign up the same student again
        Assert: Returns 400 bad request error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_increments_participant_count(self, client):
        """
        Arrange: Get initial participant count
        Act: Sign up a new student
        Assert: Participant count increased by one
        """
        # Arrange
        activity_name = "Art Studio"
        email = "newartist@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1
