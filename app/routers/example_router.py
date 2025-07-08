from fastapi import APIRouter

router = APIRouter(
    prefix="/example",
    tags=["example"]
)

@router.get("/")
def example_root():
    return {"message": "This is an example endpoint."} 