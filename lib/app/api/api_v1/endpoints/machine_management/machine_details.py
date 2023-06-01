from typing import Any, List

from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from lib.app import crud, models, schemas, mappers
from lib.app.api import deps
from lib.app.auth.firebase_auth import AuthInterceptor
from fastapi import Depends

from lib.app.error_handling.exceptions import CustomException

jwt_bearer = AuthInterceptor()
router = APIRouter()


@router.get("/",
            response_model=mappers.UnifiedOutModel, )
def read_machines(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve machines.
    """
    out_model = mappers.UnifiedOutModel()
    db_machines = crud.machine_management.machine_detail.get_multi(db=db, skip=skip, limit=limit)

    if db_machines is None:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Machines not found")
    else:
        out_model.machines = db_machines
        return out_model


@router.post("/", response_model=mappers.UnifiedOutModel, )
def create_machine(
        *,
        db: Session = Depends(deps.get_db),
        machine_in: mappers.UnifiedInModel,
) -> Any:
    """
    Create new machine with details.
    """
    out_model = mappers.UnifiedOutModel()
    machine_data = machine_in.machine_detail

    if machine_data is not None:
        machine_out = crud.machine_management.machine_detail.create_with_owner(db, obj_in=machine_data)

        if machine_out is not None:
            out_model.machines = [machine_out]
            return out_model
        else:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  detail="Error creating machine details")
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")


@router.get("/get_machine_by_id",
            response_model=mappers.UnifiedOutModel, )
def read_machine_by_id(
        db: Session = Depends(deps.get_db),
        machine_id: str = "",
) -> Any:
    """
    Retrieve machine by machine_id.
    """
    out_model = mappers.UnifiedOutModel()
    machines_list = list()

    if machine_id:
        machine_out = crud.machine_management.machine_detail.get_by_id(
            db, machine_id=machine_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")

    if machine_out is not None:
        machines_list.append(machine_out)
        out_model.machines = machines_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Machine detail for '%s' not found" % machine_id)


@router.get("/get_machine_by_name",
            response_model=mappers.UnifiedOutModel, )
def read_machine_by_name(
        db: Session = Depends(deps.get_db),
        machine: str = "",
) -> Any:
    """
    Retrieve machine by machine_name : machine.
    """
    out_model = mappers.UnifiedOutModel()
    machines_list = list()

    if machine:
        machine_out = crud.machine_management.machine_detail.get_by_machine_name(
            db, machine_name=machine)

    if machine_out is not None:
        machines_list.append(machine_out)
        out_model.machines = machines_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Machine detail for '%s' not found" % machine)


@router.put("/update", response_model=mappers.UnifiedOutModel)
def update_machine_details(
        *,
        db: Session = Depends(deps.get_db),
        in_model: mappers.UnifiedInModel,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a machine details.
    """
    out_model = mappers.UnifiedOutModel()

    machines_list = list()
    if in_model.machine_detail is not None:
        machine_id = in_model.machine_detail.id
        machine_data = crud.machine_management.machine_detail.get_by_id(db, machine_id=machine_id)

        if machine_data:
            machine_out = crud.machine_management.machine_detail.update(
                db, db_obj=machine_data, obj_in=in_model.machine_detail)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Machine details for '%s' not found" % machine_id)

        if machine_out is not None:
            machines_list.append(machine_out)
            out_model.machines = machines_list
            return out_model
        else:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  detail="Error updating machine details for '%s' " % machine_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")


@router.delete("/", response_model=mappers.UnifiedOutModel, )
def delete_machine_details(
        *,
        db: Session = Depends(deps.get_db),
        machine_id: str,
) -> Any:
    """
    Delete machine details.
    """
    out_model = mappers.UnifiedOutModel()
    machines_list = list()

    if machine_id:
        machine_out = crud.machine_management.machine_detail.get_by_id(
            db, machine_id=machine_id)

        if machine_out:
            deleted_data = crud.machine_management.machine_detail.remove_by_id(
                db, machine_id=machine_id)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Machine details for '%s' not found" % machine_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")

    if deleted_data is not None:
        machines_list.append(machine_out)
        out_model.machines = machines_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error deleting machine details for '%s' " % machine_id)
