from fastapi import Depends, HTTPException, Request, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user

request_log = {}
def get_rate_limiter(request: Request, user = Depends(get_current_user)):
    client_ip = request.client.host
    today = datetime.now().date()

    if user:
        return
    else:
        if client_ip not in request_log:
            request_log[client_ip] = {"date": today, "count": 1}
        else:
            log = request_log[client_ip]
            if log["date"] == today:
                if log["count"] >= 10:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Try again tomorrow."
                    )
                log["count"] += 1
            else:
                request_log[client_ip] = {"date": today, "count": 1}
