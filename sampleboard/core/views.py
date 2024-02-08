from rest_framework import generics
from .models import Marker, SampleBoard, Type
from .serializers import MarkerSerializer, SampleBoardSerializer, TypeSerializer

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
    serializer_class = SampleBoardSerializer

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return SampleBoard.objects.filter(uuid=uuid)


class TypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer