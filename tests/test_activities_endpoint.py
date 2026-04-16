"""Tests for GET /activities endpoint"""


class TestGetActivities:
    """Test suite for retrieving all activities"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Response contains all activities with correct structure
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities_data = response.json()
        assert isinstance(activities_data, dict)
        assert len(activities_data) > 0
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data
    
    def test_get_activities_contains_required_fields(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Each activity has required fields
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_details in activities_data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)
    
    def test_get_activities_participants_are_emails(self, client):
        """
        Arrange: No setup needed
        Act: Make GET request to /activities
        Assert: Participants list contains valid email strings
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_details in activities_data.items():
            for participant in activity_details["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant
