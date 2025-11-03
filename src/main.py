from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.storage import router as storage_router
from src.external_api import router as external_router

app = FastAPI(title="Library Storage API + Dogs External API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(storage_router.router)
app.include_router(external_router.router)

@app.get("/")
def root():
    """ Головний ендпоінт, який повертає статус та посилання на документацію. """
    return {"ok": True, "docs": "/docs"}
