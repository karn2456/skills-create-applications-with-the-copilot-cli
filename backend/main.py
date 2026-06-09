from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.config import settings
from app.routers import agents, research, literature, analysis, publications, aviation

app = FastAPI(
    title="AROS - Aviation Research Operating System",
    description="AI-Powered Aviation Research Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(research.router, prefix="/api/v1/research", tags=["Research"])
app.include_router(literature.router, prefix="/api/v1/literature", tags=["Literature"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(publications.router, prefix="/api/v1/publications", tags=["Publications"])
app.include_router(aviation.router, prefix="/api/v1/aviation", tags=["Aviation"])

@app.get("/", tags=["Health"])
async def root():
    return {"message": "AROS API is running", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "AROS Backend"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
