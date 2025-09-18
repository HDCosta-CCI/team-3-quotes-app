from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user
from dto.response_dto import GlobalResponse
from services.author_services import AuthorServices

router = APIRouter(
    prefix='/authors',
    tags=['authors']
)

@router.get("")
def fetch_all_authors(db: Session = Depends(get_db), user = Depends(get_current_user)):
    data = AuthorServices(db, user).fetch_authors()

    return GlobalResponse(
        data = data,
        message="Author fetched successfully",
        success=True
    )
