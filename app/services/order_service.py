from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.orders import Order, OrderItem
from app.schemas.orders import OrderCreate


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(
        self, order_in: OrderCreate, created_by: Optional[UUID] = None
    ) -> Order:
        db_order = Order(
            client_id=order_in.client_id,
            notes=order_in.notes,
            created_by=created_by,
            status="pending",  # Initial status
            total_amount=0,  # Will be calculated
        )
        self.db.add(db_order)
        await self.db.flush()  # To get order_id

        total_amount = 0
        for item in order_in.items:
            db_item = OrderItem(
                order_id=db_order.order_id,
                device_id=item.device_id,
                product_key=item.product_key,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            self.db.add(db_item)
            total_amount += item.quantity * item.unit_price

        db_order.total_amount = total_amount
        await self.db.commit()
        await self.db.refresh(db_order, attribute_names=["items"])
        return db_order

    async def get_order(self, order_id: UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.order_id == order_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_orders_by_client(self, client_id: UUID) -> List[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.client_id == client_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
