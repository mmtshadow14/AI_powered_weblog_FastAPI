# Python packages
from datetime import datetime, timedelta

# Celery
from celery import Celery

# App Configs
from core.config import settings

# accounts app models
from accounts.models import Otp

# posts app models
from posts.models import Post

# AI
from AI.ai_funcs import get_keywords

# DB
from core.database import Session

# DB instance
db = Session()

celery_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0', )


# remove expired otp codes
@celery_app.task
def remove_expired_otp():
    """
    this celery beat task runs every 60 seconds and deletes expired OTP codes.
    """
    expiration_time = datetime.utcnow() - timedelta(minutes=1)
    expired_otps = db.query(Otp).filter(Otp.created_at < expiration_time).all()
    for otp in expired_otps:
        db.delete(otp)
    db.commit()
    print("============================================")
    print("Expired OTPs removed")
    print("============================================")


@celery_app.task
def create_new_post(user_id, post_title, post_description):
    keywords = get_keywords(post_description)
    new_post = Post(user=user_id, title=post_title, description=post_description, tags=keywords)
    print('============================')
    print(new_post.tags)
    print('============================')
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


celery_app.conf.beat_schedule = {
    "remove-expired-otp-every-1-min": {
        "task": "core.celery_conf.remove_expired_otp",
        "schedule": 60.0,
    },
}
