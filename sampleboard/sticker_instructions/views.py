from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.response import Response

from core.models import SampleBoard, Marker
from core.serializers import SampleBoardSerializer, MarkerSerializer
from .models import InstructionsPDF, Sticker, HTMLCode
from .serializers import InstructionsPDFSerializer, StickerSerializer, HTMLCodeSerializer



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


class HTMLCodeListCreateAPIView(generics.ListCreateAPIView):
    queryset = HTMLCode.objects.all()
    serializer_class = HTMLCodeSerializer


class HTMLCodeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HTMLCode.objects.all()
    serializer_class = HTMLCodeSerializer


class StickerHTMLCodeListBySampleBoard(generics.ListAPIView):
    serializer_class = StickerSerializer

    def get_queryset(self):
        sample_board_uuid = self.kwargs['uuid']
        # Filter stickers based on the provided sample board id
        return Sticker.objects.filter(sample_board__uuid=sample_board_uuid).order_by('order')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Get the sample board data
        sample_board_uuid = self.kwargs['uuid']
        sample_board = SampleBoard.objects.get(uuid=sample_board_uuid)
        sample_board_serializer = SampleBoardSerializer(sample_board)

        # Get HTML code associated with the sample board
        html_code = HTMLCode.objects.filter(sample_board=sample_board)
        print(html_code)
        html_code_data = HTMLCodeSerializer(html_code, many=True).data if html_code else []

        # Create a combined response with stickers and sample board data
        response_data = {
            
            'sample_board': sample_board_serializer.data,
            'stickers': serializer.data,
            'html_code': html_code_data
        }

        return Response(response_data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        sticker_updates = request.data.get('sticker_updates', [])

        if not sticker_updates:
            return Response({'message': 'No sticker updates provided'}, status=status.HTTP_400_BAD_REQUEST)

        for update in sticker_updates:
            sticker_id = update.get('sticker_id')
            new_order = update.get('new_order')

            if sticker_id is None or new_order is None:
                return Response({'message': 'Both sticker_id and new_order are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                sticker = Sticker.objects.get(id=sticker_id)
            except Sticker.DoesNotExist:
                return Response({'message': f'Sticker with id {sticker_id} not found'}, status=status.HTTP_404_NOT_FOUND)

            sticker.order = new_order
            sticker.save()

        return Response({'message': 'Sticker orders updated successfully'}, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        sticker_ids_to_delete = request.data.get('sticker_ids', [])

        if not sticker_ids_to_delete:
            return Response({'message': 'No sticker IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_stickers = []
        for sticker_id in sticker_ids_to_delete:
            try:
                sticker = Sticker.objects.get(id=sticker_id)
                sticker.delete()
                deleted_stickers.append(sticker_id)
            except Sticker.DoesNotExist:
                pass  # If sticker not found, just continue to the next sticker ID

        if deleted_stickers:
            return Response({'message': f'Stickers with IDs {deleted_stickers} deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No stickers found with provided IDs'}, status=status.HTTP_404_NOT_FOUND)


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
        return Sticker.objects.filter(sample_board__marker_id=marker_id).order_by('order')

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
        
        # Get HTML code associated with the sample board
        

        # Combine stickers, marker, instructions PDFs, and sample board data
        response_data = {
            'marker': marker_serializer.data,
            'instructions_pdfs': instructions_pdfs_serializer.data,
            'sample_boards': []
        }

        for sample_board_data in sample_board_serializer.data:
            html_codes = HTMLCode.objects.filter(sample_board=sample_board_data['id'])
            html_code_data = HTMLCodeSerializer(html_codes, many=True).data if html_codes else None
        
            sample_board_data['stickers'] = sticker_serializer.data
            sample_board_data['html_codes'] = html_code_data
            response_data['sample_boards'].append(sample_board_data)

        return Response(response_data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        sticker_updates = request.data.get('sticker_updates', [])

        if not sticker_updates:
            return Response({'message': 'No sticker updates provided'}, status=status.HTTP_400_BAD_REQUEST)

        for update in sticker_updates:
            sticker_id = update.get('sticker_id')
            new_order = update.get('new_order')

            if sticker_id is None or new_order is None:
                return Response({'message': 'Both sticker_id and new_order are required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                sticker = Sticker.objects.get(id=sticker_id)
            except Sticker.DoesNotExist:
                return Response({'message': f'Sticker with id {sticker_id} not found'}, status=status.HTTP_404_NOT_FOUND)

            sticker.order = new_order
            sticker.save()

        return Response({'message': 'Sticker orders updated successfully'}, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        sticker_ids_to_delete = request.data.get('sticker_ids', [])

        if not sticker_ids_to_delete:
            return Response({'message': 'No sticker IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_stickers = []
        for sticker_id in sticker_ids_to_delete:
            try:
                sticker = Sticker.objects.get(id=sticker_id)
                sticker.delete()
                deleted_stickers.append(sticker_id)
            except Sticker.DoesNotExist:
                pass  # If sticker not found, just continue to the next sticker ID

        if deleted_stickers:
            return Response({'message': f'Stickers with IDs {deleted_stickers} deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No stickers found with provided IDs'}, status=status.HTTP_404_NOT_FOUND)