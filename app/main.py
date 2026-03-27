from fastapi import FastAPI
from app.routers.products import router as products_router

app = FastAPI(title="WhatsApp AI Bot Backend")


@app.get("/")
async def root():
    return {"message": "Backend is running"}


app.include_router(products_router)