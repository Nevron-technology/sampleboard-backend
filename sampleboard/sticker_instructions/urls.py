from django.urls import path
from .views import  HTMLCodeListCreateAPIView, HTMLCodeDetailAPIView, StickersAndInstructionsByMarker, InstructionsPDFListByMarker, StickerListBySampleBoard, InstructionsPDFListCreateAPIView, InstructionsPDFDetailAPIView, StickerListCreateAPIView, StickerDetailAPIView

urlpatterns = [
    path('instructionpdfs/', InstructionsPDFListCreateAPIView.as_view(), name='instructionpdf-list-create'),
    path('instructionpdfs/<int:pk>/', InstructionsPDFDetailAPIView.as_view(), name='instructionpdf-detail'),
    path('stickers/', StickerListCreateAPIView.as_view(), name='sticker-list-create'),
    path('stickers/<int:pk>/', StickerDetailAPIView.as_view(), name='sticker-detail'),
    path('sampleboard/<uuid:uuid>/stickers-html-code/', StickerListBySampleBoard.as_view(), name='sampleboard-stickers'),
    path('markers/<int:marker_id>/instructions_pdfs/', InstructionsPDFListByMarker.as_view(), name='instructions_pdf_list_by_marker'),
    path('markers/<int:marker_id>/combined_data/', StickersAndInstructionsByMarker.as_view(), name='combined_data_by_marker'),
    path('html-code/', HTMLCodeListCreateAPIView.as_view(), name='html-code-list'),
    path('html-code/<int:pk>/', HTMLCodeDetailAPIView.as_view(), name='html-code-details'),
]