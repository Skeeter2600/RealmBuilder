from fastapi import APIRouter

router = APIRouter(
    tags=['Startup']
)


@router.get("/", tags=["Online"])
async def hello_world():
    return dict({'message': 'Ready to go'})
