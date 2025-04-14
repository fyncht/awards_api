from django.urls import path
from .views import RewardListView, RewardRequestView

urlpatterns = [
    path('rewards/', RewardListView.as_view(), name='rewards_list'),
    path('rewards/request/', RewardRequestView.as_view(), name='reward_request'),
]
