from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import generics, status
from rest_framework.response import Response


from PIL import Image, ImageDraw, ImageFont

from core.models import SampleBoard, Marker
from core.serializers import SampleBoardSerializer, MarkerSerializer
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


class StickerListBySampleBoard(generics.ListAPIView):
    serializer_class = StickerSerializer

    def get_queryset(self):
        sample_board_uuid = self.kwargs['uuid']
        # Filter stickers based on the provided sample board id
        return Sticker.objects.filter(sample_board__uuid=sample_board_uuid)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Get the sample board data
        sample_board_uuid = self.kwargs['uuid']
        sample_board = SampleBoard.objects.get(uuid=sample_board_uuid)
        sample_board_serializer = SampleBoardSerializer(sample_board)

        # Create a combined response with stickers and sample board data
        response_data = {
            
            'sample_board': sample_board_serializer.data,
            'stickers': serializer.data
        }

        return Response(response_data)


class InstructionsPDFListByMarker(generics.ListAPIView):
    serializer_class = InstructionsPDFSerializer

    def get_queryset(self):
        marker_id = self.kwargs['marker_id']
        return InstructionsPDF.objects.filter(marker_id=marker_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Get the marker data
        marker_id = self.kwargs['marker_id']
        marker = Marker.objects.get(id=marker_id)
        # Assuming you have a serializer for the Marker model
        marker_serializer = MarkerSerializer(marker)

        # Create a combined response with instructions PDFs and marker data
        response_data = {
            'marker': marker_serializer.data,
            'instructions_pdfs': serializer.data
        }

        return Response(response_data)


class StickersAndInstructionsByMarker(generics.ListAPIView):
    serializer_class = StickerSerializer

    def get_queryset(self):
        marker_id = self.kwargs['marker_id']
        return Sticker.objects.filter(sample_board__marker_id=marker_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        sticker_serializer = self.get_serializer(queryset, many=True)

        # Get the marker data
        marker_id = self.kwargs['marker_id']
        marker = Marker.objects.get(id=marker_id)
        marker_serializer = MarkerSerializer(marker)

        # Get instructions PDFs data
        instructions_pdfs_queryset = InstructionsPDF.objects.filter(marker_id=marker_id)
        instructions_pdfs_serializer = InstructionsPDFSerializer(instructions_pdfs_queryset, many=True)

        # Get sample board data
        sample_board_queryset = SampleBoard.objects.filter(marker_id=marker_id)
        sample_board_serializer = SampleBoardSerializer(sample_board_queryset, many=True)

         # Combine stickers, marker, instructions PDFs, and sample board data
        response_data = {
            'marker': marker_serializer.data,
            'instructions_pdfs': instructions_pdfs_serializer.data,
            'sample_boards': []
        }

        for sample_board_data in sample_board_serializer.data:
            sample_board_data['stickers'] = sticker_serializer.data
            response_data['sample_boards'].append(sample_board_data)

        return Response(response_data)
