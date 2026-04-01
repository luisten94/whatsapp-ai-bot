import asyncio
from app.db.mongo import products_collection

async def seed():
    products = [
        {
            "sku": "SKU001",
            "name": "Wireless Mouse",
            "brand": "Logitech",
            "category": "Electronics",
            "price": 29.99,
            "stock": 100,
            "colors": ["Black", "White"],
            "description": "A high-precision wireless mouse with ergonomic design.",
            "active": True
        },
        {
            "sku": "SKU002",
            "name": "Bluetooth Headphones",
            "brand": "Sony",
            "category": "Electronics",
            "price": 99.99,
            "stock": 50,
            "colors": ["Black", "Blue"],
            "description": "Noise-cancelling over-ear headphones with long battery life.",
            "active": True
        },
        {
            "sku": "SKU003",
            "name": "Smartphone Stand",
            "brand": "Anker",
            "category": "Accessories",
            "price": 19.99,
            "stock": 200,
            "colors": ["Silver", "Space Gray"],
            "description": "Adjustable smartphone stand for desk use.",
            "active": True
        }
    ]

    await products_collection.delete_many({})
    await products_collection.insert_many(products)
    print("seed completed")

asyncio.run(seed())