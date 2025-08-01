from fastapi import FastAPI
from app.routes.routes import router
from app.database.database import init_db

app = FastAPI(title="Math Microservice")

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(router)
