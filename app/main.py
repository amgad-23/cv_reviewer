from fastapi import FastAPI, Depends

from app.db import Base, engine
from app.routers import upload, query, chatbot
from app.core.redis_client import redis_service
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

Base.metadata.create_all(bind=engine)
docs_url = '/swagger'
app = FastAPI(title="CV Analysis Backend", docs_url=docs_url)
rate_dependencies = [Depends(RateLimiter(times=5, seconds=60))]


@app.on_event("startup")
async def on_startup():
    await FastAPILimiter.init(redis_service.redis_client)


app.include_router(upload.router, prefix="/v1", tags=["Upload"], dependencies=rate_dependencies)
app.include_router(query.router, prefix="/v1", tags=["Query"], dependencies=rate_dependencies)
app.include_router(chatbot.router, prefix="/v1", tags=["Chatbot"], dependencies=rate_dependencies)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
