from fastapi import FastAPI
from src.storage.router import router as storage_router

app = FastAPI(
    title="Library Storage API",
    description="REST API for working with Azure Blob Storage",
    version="1.0.0"
)

app.include_router(storage_router)

@app.get("/")
async def root():
    return {
        "message": "Library Storage API", 
        "version": "1.0.0",
        "endpoints": {
            "upload_file": "POST /storage/files",
            "list_files": "GET /storage/files", 
            "download_file": "GET /storage/files/{filename}",
            "delete_file": "DELETE /storage/files/{filename}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)