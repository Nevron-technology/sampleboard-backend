from rest_framework import generics
from .models import Marker, SampleBoard
from .serializers import MarkerSerializer, SampleBoardSerializer

class MarkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer


class MarkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer


class SampleBoardListCreateAPIView(generics.ListCreateAPIView):
    queryset = SampleBoard.objects.all()
    serializer_class = SampleBoardSerializer


class SampleBoardDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SampleBoard.objects.all()
    serializer_class = SampleBoardSerializer
