from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Common"])

@router.get("/")
async def root():
    return {"message": "Hello from FastAPI Library API!"}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Library API"}