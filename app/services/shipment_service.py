from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.shipments import Shipment
from app.schemas.shipments import ShipmentCreate


class ShipmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_shipment(self, shipment_in: ShipmentCreate) -> Shipment:
        db_shipment = Shipment(
            order_id=shipment_in.order_id,
            client_id=shipment_in.client_id,
            shipping_carrier=shipment_in.shipping_carrier,
            tracking_number=shipment_in.tracking_number,
            address=shipment_in.address,
            status="pending",
        )
        self.db.add(db_shipment)
        await self.db.commit()
        await self.db.refresh(db_shipment)
        return db_shipment

    async def update_status(self, shipment_id: UUID, status: str) -> Optional[Shipment]:
        stmt = select(Shipment).where(Shipment.shipment_id == shipment_id)
        result = await self.db.execute(stmt)
        shipment = result.scalar_one_or_none()
        if shipment:
            shipment.status = status
            await self.db.commit()
            await self.db.refresh(shipment)
        return shipment

    async def get_shipments_by_client(self, client_id: UUID) -> List[Shipment]:
        stmt = select(Shipment).where(Shipment.client_id == client_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
