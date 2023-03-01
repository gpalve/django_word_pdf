from django.urls import path
from .views import upload_word,upload_xls,index,upload_pdf,remove_background_view,upload_file

urlpatterns = [
    path('', index, name='index'),
    path('word/', upload_word, name='wordupload_word'),
    path('xls/', upload_xls, name='upload_xls'),
    path('pdf/', upload_pdf, name='upload_pdf'),
    path('ppt/', upload_file, name='upload_pdf'),
    path('bgremover/', remove_background_view, name='remove_background_view'),

    
]
