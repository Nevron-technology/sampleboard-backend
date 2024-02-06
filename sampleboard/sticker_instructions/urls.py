from django.urls import path
from .views import InstructionsPDFListCreateAPIView, InstructionsPDFDetailAPIView, StickerListCreateAPIView, StickerDetailAPIView

urlpatterns = [
    path('instructionpdfs/', InstructionsPDFListCreateAPIView.as_view(), name='instructionpdf-list-create'),
    path('instructionpdfs/<int:pk>/', InstructionsPDFDetailAPIView.as_view(), name='instructionpdf-detail'),
    path('stickers/', StickerListCreateAPIView.as_view(), name='sticker-list-create'),
    path('stickers/<int:pk>/', StickerDetailAPIView.as_view(), name='sticker-detail'),
]