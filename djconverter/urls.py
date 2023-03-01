from django.urls import path
from .views import upload_word,upload_xls,index

urlpatterns = [
    path('', index, name='index'),
    path('word/', upload_word, name='wordupload_word'),
    path('xls/', upload_xls, name='upload_xls'),
]
