from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.db.mongo import products_collection
from app.schemas.product import ProductCreate

router = APIRouter(prefix="/products", tags=["products"])


def product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "sku": product["sku"],
        "name": product["name"],
        "brand": product["brand"],
        "category": product["category"],
        "price": product["price"],
        "stock": product["stock"],
        "colors": product.get("colors", []),
        "description": product.get("description"),
        "active": product.get("active", True),
        "created_at": product.get("created_at"),
    }


@router.post("/")
async def create_product(product: ProductCreate):
    new_product = product.model_dump()
    new_product["created_at"] = datetime.utcnow()

    result = await products_collection.insert_one(new_product)
    created_product = await products_collection.find_one({"_id": result.inserted_id})

    return product_serializer(created_product)


@router.get("/")
async def list_products():
    products = []
    cursor = products_collection.find()

    async for product in cursor:
        products.append(product_serializer(product))

    return products


@router.get("/{product_id}")
async def get_product(product_id: str):
    try:
        product = await products_collection.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_serializer(product)