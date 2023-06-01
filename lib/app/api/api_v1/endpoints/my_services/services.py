from typing import Any, List

from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from lib.app import crud, models, schemas, mappers
from lib.app.api import deps
from fastapi import Depends

from lib.app.error_handling.exceptions import CustomException

router = APIRouter()


@router.post("/create_service",
             response_model=mappers.UnifiedOutModel,
             response_model_exclude_none=True,)
def create_service(
        *,
        db: Session = Depends(deps.get_db),
        service_detail_in: mappers.UnifiedInModel,
) -> Any:
    """
    Create new service
    """
    out_model = mappers.UnifiedOutModel()
    service_detail = crud.service_detail.create_with_owner(db=db, obj_in=service_detail_in.service_detail)

    if service_detail is not None:
        out_model.service_details = [service_detail]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error creating service details")
