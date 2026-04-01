from app.db.mongo import products_collection

async def find_productg_by_name(name: str):
    return await products_collection.find_one({"name": {"$regex": name, "$options": "i"},
                                               "active": True
                                               })

async def find_in_stock_product_by_name(name: str):
    return await products_collection.find_one({"name": {"$regex": name, "$options": "i"},
                                               "active": True,
                                               "stock": {"$gt": 0}
                                               })