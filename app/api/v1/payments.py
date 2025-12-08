from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import ResponseModel
from app.schemas.payments import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService

from app.api.deps import get_current_user
from app.models.users import User

router = APIRouter()


@router.post(
    "/payments",
    response_model=ResponseModel[PaymentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    payment_in: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaymentService(db)
    payment = await service.create_payment(payment_in)
    return ResponseModel(message="Payment created successfully", data=payment)


@router.get("/payments/{payment_id}", response_model=ResponseModel[PaymentResponse])
async def get_payment(
    payment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaymentService(db)
    payment = await service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return ResponseModel(message="Payment retrieved successfully", data=payment)


@router.get(
    "/clients/{client_id}/payments", response_model=ResponseModel[List[PaymentResponse]]
)
async def get_client_payments(
    client_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaymentService(db)
    payments = await service.get_payments_by_client(client_id)
    return ResponseModel(message="Payments retrieved successfully", data=payments)
