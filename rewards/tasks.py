from celery import shared_task
from django.utils import timezone
from django.db import transaction
from .models import ScheduledReward, RewardLog

@shared_task
def process_scheduled_reward(scheduled_reward_id):
    try:
        scheduled_reward = ScheduledReward.objects.get(id=scheduled_reward_id, executed=False)
        # Выполняем задачу, только если время выполнения достигнуто
        if timezone.now() >= scheduled_reward.execute_at:
            with transaction.atomic():
                user = scheduled_reward.user
                user.coins += scheduled_reward.amount
                user.save()
                RewardLog.objects.create(user=user, amount=scheduled_reward.amount)
                scheduled_reward.executed = True
                scheduled_reward.save()
    except ScheduledReward.DoesNotExist:
        pass
