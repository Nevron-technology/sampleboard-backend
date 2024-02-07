from django.urls import path
from .views import MarkerListCreateAPIView, MarkerDetailAPIView, SampleBoardListCreateAPIView, SampleBoardDetailAPIView

urlpatterns = [
    path('markers/', MarkerListCreateAPIView.as_view(), name='marker-list-create'),
    path('markers/<int:pk>/', MarkerDetailAPIView.as_view(), name='marker-detail'),
    path('sampleboards/', SampleBoardListCreateAPIView.as_view(), name='sampleboard-list-create'),
    path('sampleboards/<uuid:uuid>/', SampleBoardDetailAPIView.as_view(), name='sampleboard-detail'),
]