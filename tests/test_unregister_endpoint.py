"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""


class TestUnregisterEndpoint:
    """Test suite for activity unregistration functionality"""
    
    def test_unregister_removes_participant_from_activity(self, client):
        """
        Arrange: Select an activity with registered students
        Act: Unregister a student
        Assert: Student is removed from participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify participant was actually removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_returns_success_message(self, client):
        """
        Arrange: Prepare unregister request
        Act: Send unregister request
        Assert: Response contains success message
        """
        # Arrange
        activity_name = "Debate Team"
        email = "noah@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_unregister_fails_for_nonexistent_activity(self, client):
        """
        Arrange: Prepare unregister for non-existent activity
        Act: Attempt unregister
        Assert: Returns 404 not found error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_fails_if_student_not_registered(self, client):
        """
        Arrange: A student is not registered for an activity
        Act: Attempt to unregister them
        Assert: Returns 400 bad request error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_decrements_participant_count(self, client):
        """
        Arrange: Get initial participant count
        Act: Unregister a student
        Assert: Participant count decreased by one
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
