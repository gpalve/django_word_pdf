from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


class ExcelToPDF(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class PdfToTxt(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class bgr(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class PptTOPdf(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class MergePdf(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']