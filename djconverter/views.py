from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from io import BytesIO
from .forms import FileUploadForm , ExcelToPDF,PdfToTxt
from .models import UploadedFile
from docx2pdf import convert
from io import BytesIO
from django.http import FileResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import xlrd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from wand.image import Image
from wand.display import display


# This function is only for word to pdf
def index(request):
    context = {
        'form': FileUploadForm(),
        'excel_to_pdf': ExcelToPDF(),
        'pdf_to_txt': PdfToTxt()
    }
    return render(request, 'upload_form.html',context)


def upload_word(request):
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
    
      

# This is for xls file and Latest excel
def upload_xls(request):
    if request.method == 'POST':
        # Get the uploaded file from the form
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # Load the workbook from the uploaded file
            if uploaded_file.file.name.endswith('.xls'):
                workbook = xlrd.open_workbook(file_contents=uploaded_file.read())
                sheets = workbook.sheet_names()
            elif uploaded_file.file.name.endswith('.xlsx'):
                workbook = load_workbook(uploaded_file.file)
                sheets = workbook.sheetnames
            else:
                raise ValueError('Unsupported file type')
            # Create the PDF file
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            style = ParagraphStyle('table', fontSize=10, leading=12)
            table_style = TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)
            ])
            for sheet_name in sheets:
                # Get the data from the sheet
                if uploaded_file.file.name.endswith('.xls'):
                    worksheet = workbook.sheet_by_name(sheet_name)
                    data = []
                    for row_num in range(worksheet.nrows):
                        row = worksheet.row_values(row_num)
                        data.append(row)
                elif uploaded_file.file.name.endswith('.xlsx'):
                    worksheet = workbook[sheet_name]
                    data = []
                    for row in worksheet.iter_rows(values_only=True):
                        data.append(row)
                else:
                    raise ValueError('Unsupported file type')
                # Create table and apply style
                table_data = []
                for row in data:
                    table_data.append([Paragraph(str(cell), style) for cell in row])
                table = Table(table_data)
                table.setStyle(table_style)
                elements.append(table)
            # Build and save the PDF file to the default storage
            doc.build(elements)
            buffer.seek(0)
            output_file = ContentFile(buffer.getvalue())
            output_path = uploaded_file.file.name.replace('.xls', '.pdf').replace('.xlsx', '.pdf')
            default_storage.save(output_path, output_file)
            # Return the PDF file as a download
            response = FileResponse(buffer, as_attachment=True, filename=output_path)
            return response


def convert_pdf_to_images(pdf_file_path):
    with Image(filename=pdf_file_path) as pdf_image:
        return pdf_image

def upload_pdf(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # Convert the uploaded file to an image
            input_path = uploaded_file.file.path
            image = convert_pdf_to_images(input_path)
            # Perform processing on the image here
            # ...
            # Return the image as a download
            with open(image.filename, 'rb') as image_file:
                image_bytes = image_file.read()
            image_file = BytesIO(image_bytes)
            response = FileResponse(image_file, as_attachment=True, filename=uploaded_file.file.name.replace('.pdf', '.png'))
            return response
        
def my_view(request):
    file_upload_form = FileUploadForm()
    contact_form = ExcelToPDF()
    context = {
        'file_upload_form': file_upload_form,
        'contact_form': contact_form
    }
    return render(request, 'my_template.html', context)