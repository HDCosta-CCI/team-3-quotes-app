from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies.get_db import get_db
from services.quote_services import QuoteServices
from dotenv import load_dotenv
import os

load_dotenv()
SCHEDULER_TIME = int(os.getenv("SCHEDULER_TIME"))


def create_scheduler():
    return AsyncIOScheduler()

def add_jobs(scheduler):
    db = next(get_db())
    trigger = CronTrigger(second=f"*/{SCHEDULER_TIME}")
    # trigger = CronTrigger(minute="*/10")
    scheduler.add_job(QuoteServices(db, user=None).count_like_dislike, trigger, id="count_job", replace_existing=True)
