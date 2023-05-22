def test_that_api_is_working(test_app):
    """Test to verify that the API is running."""
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Consultation API! Please note that before the API can be used, "
        "you would have to set the maximum power of the site. "
        "This can be done by sending a POST request to the /api/v1/maximum-power endpoint."
    }
