from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="My FastAPI Project")

# Include router din endpoint-uri
app.include_router(router)
