from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies.get_db import get_db
from services.quote_services import QuoteServices


def create_scheduler():
    return AsyncIOScheduler()

def add_jobs(scheduler):
    db = next(get_db())
    trigger = CronTrigger(second="*/20")
    # trigger = CronTrigger(minute="*/10")
    scheduler.add_job(QuoteServices(db, user=None).count_like_dislike, trigger, id="count_job", replace_existing=True)


