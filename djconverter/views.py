from django.shortcuts import render
from django.http import FileResponse
from io import BytesIO
from .forms import FileUploadForm
from .models import UploadedFile
from docx2pdf import convert

# This function is only for word to pdf
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # Perform processing on the uploaded file here
            input_path = uploaded_file.file.path
            output_path = input_path.replace('.docx', '.pdf')
            convert(input_path, output_path)
            # Return the PDF file as a download
            with open(output_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            pdf_file = BytesIO(pdf_bytes)
            response = FileResponse(pdf_file, as_attachment=True, filename=uploaded_file.file.name.replace('.docx', '.pdf'))
            return response
    else:
        form = FileUploadForm()
    return render(request, 'upload_form.html', {'form': form})

# This is for xls
def upload_xls():
    return