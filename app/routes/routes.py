from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import AsyncSessionLocal
from app.services.services import power, fibonacci, factorial
from app.models.models import RequestLog
from app.schemas.schemas import MathRequest, MathResponse
from app.logger.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from sqlalchemy import text



router = APIRouter()

# Dependency to get DB session per request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/health", tags=["System"], summary="Health check for API and DB")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))  # ✅ wrap SQL in text()
        return {"status": "ok", "message": "Service is healthy ✅"}
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Database connection failed", "details": str(e)}
        )

    
@router.post("/pow", response_model=MathResponse)
async def compute_power(data: MathRequest, db: AsyncSession = Depends(get_db)):
    if data.y is None:
        raise HTTPException(status_code=400, detail="Missing 'y' for power function")
    result = power(data.x, data.y)
    logger.info(f"Power request: {data.x}^{data.y} = {result}")
    log = RequestLog(operation="power", input=f"{data.x}^{data.y}", result=result)
    db.add(log)
    await db.commit()
    return MathResponse(operation="power", input=f"{data.x}^{data.y}", result=result)

@router.post("/fibonacci", response_model=MathResponse)
async def compute_fibonacci(data: MathRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = fibonacci(data.x)
        logger.info(f"Power request: {data.x}^{data.y} = {result}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    log = RequestLog(operation="fibonacci", input=str(data.x), result=result)
    db.add(log)
    await db.commit()
    return MathResponse(operation="fibonacci", input=str(data.x), result=result)

@router.post("/factorial", response_model=MathResponse)
async def compute_factorial(data: MathRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = factorial(data.x)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    log = RequestLog(operation="factorial", input=str(data.x), result=result)
    db.add(log)
    await db.commit()
    return MathResponse(operation="factorial", input=str(data.x), result=result)

