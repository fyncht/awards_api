from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ScheduledReward
from .tasks import process_scheduled_reward


@receiver(post_save, sender=ScheduledReward)
def schedule_reward_task(sender, instance, created, **kwargs):
    if created and not instance.executed:
        # Рассчитываем задержку в секундах от текущего времени до execute_at
        delay = (instance.execute_at - timezone.now()).total_seconds()
        if delay < 0:
            delay = 0
        process_scheduled_reward.apply_async((instance.id,), countdown=delay)
