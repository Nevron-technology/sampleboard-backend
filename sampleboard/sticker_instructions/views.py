from rest_framework import generics
from .models import InstructionsPDF, Sticker
from .serializers import InstructionsPDFSerializer, StickerSerializer

class InstructionsPDFListCreateAPIView(generics.ListCreateAPIView):
    queryset = InstructionsPDF.objects.all()
    serializer_class = InstructionsPDFSerializer

class InstructionsPDFDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InstructionsPDF.objects.all()
    serializer_class = InstructionsPDFSerializer

class StickerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer

class StickerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer
