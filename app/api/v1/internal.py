from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.core.paseto import create_nexus_token
from app.models.users import User
from app.schemas.common import ResponseModel

router = APIRouter()


@router.post(
    "/internal/tokens/nexus",
    response_model=ResponseModel[str],
    dependencies=[Depends(require_roles(["admin"]))],
)
async def generate_nexus_token(
    current_user: Annotated[User, Depends(require_roles(["admin"]))],
):
    """
    Genera un token PASETO para comunicación interna con Nexus.
    Solo accesible por usuarios con rol admin.

    El token expira en 5 minutos y contiene:
    - internal_id: UUID del usuario
    - service: "gac"
    - role: "NEXUS_ADMIN"
    - scope: "internal-nexus-admin"
    """
    token = create_nexus_token(user_id=current_user.user_id)
    return ResponseModel(message="Token generated successfully", data=token)
