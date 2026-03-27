from pydantic import BaseModel
from typing import Optional, List


class ProductCreate(BaseModel):
    sku: str
    name: str
    brand: str
    category: str
    price: float
    stock: int
    colors: List[str] = []
    description: Optional[str] = None
    active: bool = True