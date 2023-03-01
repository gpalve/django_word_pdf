from django.shortcuts import render
from django.http import FileResponse
from io import BytesIO
from .forms import FileUploadForm , ExcelToPDF
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
        context = {
        'form': FileUploadForm(),
        'excel_to_pdf': ExcelToPDF()
    }
    return render(request, 'upload_form.html',context)

# This is for xls file and Latest excel
def upload_xls():
    return

def my_view(request):
    file_upload_form = FileUploadForm()
    contact_form = ExcelToPDF()
    context = {
        'file_upload_form': file_upload_form,
        'contact_form': contact_form
    }
    return render(request, 'my_template.html', context)