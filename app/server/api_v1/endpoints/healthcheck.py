from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Healthcheck"], status_code=200)
async def read_root():
    """A healthcheck endpoint to check if the API is running and set up correctly."""
    return {
        "message": "Welcome to the Consultation API! Please note that before the API can be used, "
        "you would have to set the maximum power of the site. "
        "This can be done by sending a POST request to the /api/v1/maximum-power endpoint."
    }
