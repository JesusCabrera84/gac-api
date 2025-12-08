from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import ResponseModel
from app.schemas.orders import OrderCreate, OrderResponse
from app.services.order_service import OrderService

from app.api.deps import get_current_user
from app.models.users import User

router = APIRouter()


@router.post(
    "/orders",
    response_model=ResponseModel[OrderResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    created_by = current_user.user_id
    order = await service.create_order(order_in, created_by)
    return ResponseModel(message="Order created successfully", data=order)


@router.get("/orders/{order_id}", response_model=ResponseModel[OrderResponse])
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(message="Order retrieved successfully", data=order)


@router.get(
    "/clients/{client_id}/orders", response_model=ResponseModel[List[OrderResponse]]
)
async def get_client_orders(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    orders = await service.get_orders_by_client(client_id)
    return ResponseModel(message="Orders retrieved successfully", data=orders)
