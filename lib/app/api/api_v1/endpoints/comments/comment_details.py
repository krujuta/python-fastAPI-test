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
def read_comments(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve comments.
    """
    out_model = mappers.UnifiedOutModel()
    db_comments = crud.comments.comment_detail.get_multi(db=db, skip=skip, limit=limit)

    if db_comments is None:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Comments not found")
    else:
        out_model.comments = db_comments
        return out_model


@router.post("/", response_model=mappers.UnifiedOutModel, )
def create_comment(
        *,
        db: Session = Depends(deps.get_db),
        comment_in: mappers.UnifiedInModel,
) -> Any:
    """
    Create new comment with details.
    """
    out_model = mappers.UnifiedOutModel()
    comment_data = comment_in.comment_detail

    if comment_data is not None:
        comment_out = crud.comments.comment_detail.create_with_owner(db, obj_in=comment_data)

        if comment_out is not None:
            out_model.comments = [comment_out]
            return out_model
        else:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  detail="Error creating comment details")
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")


@router.get("/get_comments_by_created_user_id",
            response_model=mappers.UnifiedOutModel, )
def get_comments_by_created_user_id(
        db: Session = Depends(deps.get_db),
        created_user_id: str = "",
) -> Any:
    """
    Retrieve comments by created_user_id.
    """
    out_model = mappers.UnifiedOutModel()
    comments_list = list()

    if created_user_id:
        comment_out = crud.comments.comment_detail.get_by_created_user_id(
            db, created_user_id=created_user_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Insufficient request details")

    if comment_out is not None:
        comments_list.append(comment_out)
        out_model.comments = comments_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Comments for '%s' not found" % created_user_id)


@router.get("/get_by_comment_id",
            response_model=mappers.UnifiedOutModel, )
def read_comment_by_id(
        db: Session = Depends(deps.get_db),
        comment_id: str = "",
) -> Any:
    """
    Retrieve comment by comment id
    """
    out_model = mappers.UnifiedOutModel()
    comments_list = list()

    if comment_id:
        comment_out = crud.comments.comment_detail.get_by_id(
            db, comment_id=comment_id)

    if comment_out is not None:
        comments_list.append(comment_out)
        out_model.comments = comments_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Comment details for '%s' not found" % comment_id)


@router.put("/update", response_model=mappers.UnifiedOutModel)
def update_comment_details(
        *,
        db: Session = Depends(deps.get_db),
        in_model: mappers.UnifiedInModel,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a comment details.
    """
    out_model = mappers.UnifiedOutModel()

    comments_list = list()
    if in_model.comment_detail is not None:
        comment_id = in_model.comment_detail.id
        comment_data = crud.comments.comment_detail.get_by_id(db, comment_id=comment_id)

        if comment_data:
            comment_out = crud.comments.comment_detail.update(
                db, db_obj=comment_data, obj_in=in_model.comment_detail)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Comment details for '%s' not found" % comment_id)

        if comment_out is not None:
            comments_list.append(comment_out)
            out_model.comments = comments_list
            return out_model
        else:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  detail="Error updating comment details for '%s' " % comment_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")


@router.delete("/", response_model=mappers.UnifiedOutModel, )
def delete_comment_details(
        *,
        db: Session = Depends(deps.get_db),
        comment_id: str,
) -> Any:
    """
    Delete comment details.
    """
    out_model = mappers.UnifiedOutModel()
    comments_list = list()

    if comment_id:
        comment_out = crud.comments.comment_detail.get_by_id(
            db, comment_id=comment_id)

        if comment_out:
            deleted_data = crud.comments.comment_detail.remove_by_id(
                db, comment_id=comment_id)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Comment details for '%s' not found" % comment_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")

    if deleted_data is not None:
        comments_list.append(comment_out)
        out_model.comments = comments_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error deleting comment details for '%s' " % comment_id)
