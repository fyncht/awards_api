from rest_framework import serializers
from .models import RewardLog, ScheduledReward


class RewardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardLog
        fields = ['id', 'amount', 'given_at']


class ScheduledRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReward
        fields = ['id', 'user', 'amount', 'execute_at', 'executed']
