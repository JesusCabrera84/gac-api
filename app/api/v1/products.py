from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.schemas.common import ResponseModel
from app.api.deps import get_current_user
from app.models.users import User

router = APIRouter()


class Product(BaseModel):
    key: str
    name: str
    description: str


# In-memory database for products
products_db: List[Product] = [
    Product(key="nexus", name="Nexus", description="GPS Tracking Device"),
]


@router.get("/products", response_model=ResponseModel[List[Product]])
async def get_products(current_user: User = Depends(get_current_user)):
    return ResponseModel(message="Products retrieved successfully", data=products_db)


@router.post("/products", response_model=ResponseModel[Product])
async def create_product(
    product: Product, current_user: User = Depends(get_current_user)
):
    # Check if key already exists
    if any(p.key == product.key for p in products_db):
        # In a real app, raise 400. For now, just return existing or append?
        # Let's append or overwrite? Duplicate keys might be bad.
        # Let's raise error.
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Product key already exists")

    products_db.append(product)
    return ResponseModel(message="Product created successfully", data=product)
