from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user
from services.quote_services import QuoteServices
from dto.quotes_dto import QuoteRequest, QuoteResponse, QuoteUpdateRequest
from uuid import UUID

router = APIRouter(
    prefix='/quotes',
    tags=['quotes']
)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_quotes(db: Session = Depends(get_db)):
    try:
        data = QuoteServices(db, user=None).get_all_quotes()
        return QuoteResponse(
            success = True,
            message = "Quotes fetched successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e    


@router.get('/tags', status_code=status.HTTP_200_OK)
async def get_all_quote_tags(db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).get_quote_tags()

        return QuoteResponse (
            success = True,
            message = "Quote tags fetched successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_quote(request: QuoteRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).create_quote(request)
        return QuoteResponse (
            success = True,
            message = "Quote created successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.patch('/{quote_id}', status_code=status.HTTP_200_OK)
async def update_quote(quote_id: UUID, request: QuoteUpdateRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).update_quote(quote_id, request)
        return QuoteResponse (
            success = True,
            message = "Quote updated successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    

@router.delete('/{quote_id}', status_code=status.HTTP_200_OK)
async def delete_quote(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).delete_quote(quote_id)
        return QuoteResponse (
            success = True,
            message = "Quote deleted successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.get('/{quote_id}', status_code=status.HTTP_200_OK)
async def get_quote_by_id(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).get_quote(quote_id)
        return QuoteResponse (
            success = True,
            message = "Quote fetched successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


