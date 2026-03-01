from django.template.loader import get_template
from weasyprint import HTML
from io import BytesIO


def generate_document_pdf(document_type, document):
    template = get_template(f"{document_type}s/{document_type}_pdf.html")
    html_string = template.render({f"{document_type}": document})

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    return pdf_file
