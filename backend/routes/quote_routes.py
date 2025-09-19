from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user
from services.quote_services import QuoteServices
from dto.quotes_dto import QuoteRequest, QuoteResponse, QuoteUpdateRequest
from dto.response_dto import GlobalResponse
from uuid import UUID

router = APIRouter(
    prefix='/quotes',
    tags=['quotes']
)

@router.get(
    '', 
    status_code=status.HTTP_200_OK,
    summary="Get All Quotes",
    description="""
    Fetches a list of all available quotes in the system.  
    - Public endpoint (no authentication required)  
    - Returns a structured list of quotes including author, content, and tags
    """,
    openapi_extra={"security": []}
)
async def get_all_quotes(db: Session = Depends(get_db)):
    try:
        data = QuoteServices(db, user=None).get_all_quotes()
        return GlobalResponse(
            success = True,
            message = "Quotes fetched successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e    


@router.get(
    '/tags', 
    status_code=status.HTTP_200_OK,
    summary="Get All Quote Tags",
    description="""
    Fetches all unique tags used across quotes.  
    - Protected route (requires authentication)  
    - Useful for filtering quotes by category/tag
    """
)
async def get_all_quote_tags(db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).get_quote_tags()

        return GlobalResponse (
            success = True,
            message = "Quote tags fetched successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.post(
    '', 
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Quote",
    description="""
    Allows an authenticated user to create a new quote.  
    - Requires authentication  
    - Request must include `author`, `quote`, and optional `tags`  
    """
)
async def create_new_quote(request: QuoteRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).create_quote(request)
        return GlobalResponse (
            success = True,
            message = "Quote created successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.patch(
    '/{quote_id}', 
    status_code=status.HTTP_200_OK,
    summary="Update an Existing Quote",
    description="""
    Updates details of an existing quote by ID.  
    - Requires authentication  
    - Supports updating author, quote text, or tags
    """
)
async def update_quote(quote_id: UUID, request: QuoteUpdateRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).update_quote(quote_id, request)
        return GlobalResponse (
            success = True,
            message = "Quote updated successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    

@router.delete(
    '/{quote_id}', 
    status_code=status.HTTP_200_OK,
    summary="Delete a Quote",
    description="""
    Deletes a quote by its ID.  
    - Requires authentication  
    - Only quote owners or admins should be able to delete
    """
)
async def delete_quote(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).delete_quote(quote_id)
        return GlobalResponse (
            success = True,
            message = "Quote deleted successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    '/{quote_id}', 
    status_code=status.HTTP_200_OK,
    summary="Get Quote by ID",
    description="""
    Fetches a single quote by its unique ID.  
    - Requires authentication  
    - Returns the full quote details (author, quote, tags, user info)
    """
)
async def get_quote_by_id(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).get_quote(quote_id)
        return GlobalResponse (
            success = True,
            message = "Quote fetched successfully!",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    '/{quote_id}/like/up',
    status_code=status.HTTP_200_OK
)
async def like_quote(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:    
        data = QuoteServices(db, user).like_quote_up(quote_id)
        return GlobalResponse (
            success = True,
            message = "Quote liked successfully",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    '/{quote_id}/dislike/up',
    status_code=status.HTTP_200_OK
)
async def dislike_quote(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:    
        data = QuoteServices(db, user).dislike_quote_up(quote_id)
        return GlobalResponse (
            success = True,
            message = "Quote disliked successfully",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    '/{quote_id}/like/down',
    status_code=status.HTTP_200_OK
)
async def remove_like(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:    
        data = QuoteServices(db, user).like_quote_down(quote_id)
        return GlobalResponse (
            success = True,
            message = "Like removed successfully",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e


@router.get(
    '/{quote_id}/dislike/down',
    status_code=status.HTTP_200_OK
)
async def remove_dislike(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:    
        data = QuoteServices(db, user).dislike_quote_down(quote_id)
        return GlobalResponse (
            success = True,
            message = "Dislike removed successfully",
            data = data
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    

@router.get("/{quote_id}/like/users")
def fetch_liked_users(quote_id:UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).fetch_liked_user(quote_id)
        return GlobalResponse(
            data= data,
            message= "Users fetched successfully",
            success= True
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e

@router.get("/{quote_id}/dislike/users")
def fetch_disliked_users(quote_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        data = QuoteServices(db, user).fetch_disliked_user(quote_id)
        return GlobalResponse(
            data= data,
            message= "Users fetched successfully",
            success= True
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e    
