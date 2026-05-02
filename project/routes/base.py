from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check():
    return {"details": "Welcome to user-risk-detection-api!"}
