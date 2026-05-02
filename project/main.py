from fastapi import FastAPI
from routes import base, predict, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="User Risk Detection API",
    description="Detect user vulnerabilities risk",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base.router, tags=["User", "Risk", "Detection", "API"])
app.include_router(health.router, tags=["Health"])
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
