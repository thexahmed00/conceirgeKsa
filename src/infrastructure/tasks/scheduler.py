"""Background job scheduler for running periodic tasks."""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.infrastructure.tasks.subscription_checker import run_subscription_checker
from src.shared.logger.config import get_logger

logger = get_logger(__name__)

# Global scheduler instance
scheduler = BackgroundScheduler()


def start_scheduler():
    """Start the background scheduler with all scheduled jobs."""
    
    # Add subscription expiration checker - runs daily at 9 AM
    scheduler.add_job(
        run_subscription_checker,
        trigger=CronTrigger(hour=9, minute=0),  # 9:00 AM every day
        id="subscription_checker",
        name="Check expiring subscriptions",
        replace_existing=True,
    )
    
    logger.info("Starting background scheduler...")
    scheduler.start()
    logger.info("Background scheduler started successfully")


def stop_scheduler():
    """Stop the background scheduler gracefully."""
    if scheduler.running:
        logger.info("Stopping background scheduler...")
        scheduler.shutdown()
        logger.info("Background scheduler stopped")


def get_scheduler_status():
    """Get status of all scheduled jobs."""
    if not scheduler.running:
        return {"running": False, "jobs": []}
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": str(job.next_run_time) if job.next_run_time else None,
        })
    
    return {
        "running": True,
        "jobs": jobs,
    }
