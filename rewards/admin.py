from django.contrib import admin
from .models import ScheduledReward, RewardLog

admin.site.register(ScheduledReward)
admin.site.register(RewardLog)
