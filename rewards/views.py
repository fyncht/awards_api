from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import ScheduledReward, RewardLog
from .serializers import RewardLogSerializer, ScheduledRewardSerializer


class RewardListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reward_logs = RewardLog.objects.filter(user=request.user).order_by('-given_at')
        serializer = RewardLogSerializer(reward_logs, many=True)
        return Response(serializer.data)


class RewardRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Проверяем, делал ли пользователь запрос награды в последние 24 часа
        time_threshold = timezone.now() - timedelta(days=1)
        recent_reward = ScheduledReward.objects.filter(user=request.user, execute_at__gte=time_threshold).exists()
        if recent_reward:
            return Response({'detail': 'Вы можете запросить награду только 1 раз в сутки'}, status=400)

        # Создаем плановую награду, которая выполнится через 5 минут (например, начисляем 10 монет)
        execute_time = timezone.now() + timedelta(minutes=5)
        scheduled_reward = ScheduledReward.objects.create(user=request.user, amount=10, execute_at=execute_time)
        serializer = ScheduledRewardSerializer(scheduled_reward)
        return Response(serializer.data, status=201)
