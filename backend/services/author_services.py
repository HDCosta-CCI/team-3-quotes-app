from fastapi import HTTPException, status
from models.quotes import Quotes
class AuthorServices():
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def fetch_authors(self):
        try:
            if self.user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")
            
            authors = self.db.query(Quotes.author).distinct().all()

            if not authors:
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            author_list = [a[0] for a in authors]

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

        else:
            return author_list
