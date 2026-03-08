from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from utils.qr_generator import generate_qr_image

def generate_certificate_pdf(student_name, course, issue_date, cert_uuid, output_path):
    c = canvas.Canvas(output_path, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Border and Background
    c.setLineWidth(5)
    c.rect(20, 20, width - 40, height - 40)
    
    # Title
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2.0, height - 100, "University Certificate of Completion")

    # Body
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 200, "This is to certify that")
    
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2.0, height - 240, student_name)
    
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2.0, height - 290, f"has successfully completed the program:")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 330, course)
    
    # Issue Date
    c.setFont("Helvetica", 14)
    c.drawString(100, 100, f"Date: {issue_date}")
    c.drawString(100, 80, f"ID: {cert_uuid}")

    # Signatures
    c.drawString(width - 300, 100, "_________________________")
    c.drawString(width - 250, 80, "Authorized Signature")

    # Generate and embed QR Code
    qr_path = f"tmp_qr_{cert_uuid}.png"
    generate_qr_image(cert_uuid, qr_path)
    c.drawImage(qr_path, width - 150, height - 200, width=100, height=100)

    c.save()
