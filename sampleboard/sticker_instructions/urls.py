from django.urls import path
from .views import InstructionsPDFGenerateAPIView, StickerListBySampleBoard, InstructionsPDFListCreateAPIView, InstructionsPDFDetailAPIView, StickerListCreateAPIView, StickerDetailAPIView

urlpatterns = [
    path('instructionpdfs/', InstructionsPDFListCreateAPIView.as_view(), name='instructionpdf-list-create'),
    path('instructionpdfs/<int:pk>/', InstructionsPDFDetailAPIView.as_view(), name='instructionpdf-detail'),
    path('stickers/', StickerListCreateAPIView.as_view(), name='sticker-list-create'),
    path('stickers/<int:pk>/', StickerDetailAPIView.as_view(), name='sticker-detail'),
    path('sampleboard/<uuid:uuid>/stickers/', StickerListBySampleBoard.as_view(), name='sampleboard-stickers'),
    path('generate-pdf/', InstructionsPDFGenerateAPIView.as_view(), name='generate_pdf'),
]