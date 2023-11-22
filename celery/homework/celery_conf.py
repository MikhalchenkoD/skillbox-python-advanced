from celery import Celery
from celery.schedules import crontab

from image import blur_image
from mail import send_email_for_subscribed, send_email
from models import User

celery_app = Celery(
    "tasks",
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour='7', minute='30', day_of_week='1'),
        weekly_mailing.s(),
    )


@celery_app.task
def weekly_mailing():
    victims = User.get_subscribed_users()
    for user in victims:
        send_email_for_subscribed(user.email)


@celery_app.task(bind=True)
def process_images(self, filename: str, email: str):
    print('dasdasds')
    task_id = self.request.id
    print('dsds')
    blured_image = blur_image(filename)

    self.update_state(state='Mail sending', meta={})

    send_email(task_id, email, blured_image)

    self.update_state(state='Finished', meta={})
    return "Done"