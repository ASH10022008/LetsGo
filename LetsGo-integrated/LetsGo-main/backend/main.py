import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.services import transit_service

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "Frontend"
SIMULATION_INTERVAL_SECONDS = 2


async def _simulate_vehicles():
    while True:
        transit_service.simulate_step()
        await asyncio.sleep(SIMULATION_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(_simulate_vehicles())
    yield
    task.cancel()


app = FastAPI(
    title="Campus & City Transit API",
    version="1.0.0",
    description="Real-time campus and city transit data API.",
    lifespan=lifespan,
)

# Dev-friendly CORS so the frontend works from Live Server (5500), file://, etc.
# Restrict allow_origins to your real domain before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Campus & City Transit API is running",
        "docs": "/docs",
        "app": "/app/",
    }


# Serve the frontend from the same server: http://localhost:8000/app/
app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
