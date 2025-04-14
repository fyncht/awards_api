from django.db import models
from django.conf import settings


class ScheduledReward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    execute_at = models.DateTimeField()
    executed = models.BooleanField(default=False)

    def __str__(self):
        return f"ScheduledReward for {self.user.username} of {self.amount} at {self.execute_at}"


class RewardLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    given_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RewardLog for {self.user.username} of {self.amount} given at {self.given_at}"
