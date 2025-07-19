from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os
from datetime import datetime
import re

class PDFGenerator:
    def __init__(self):
        self.output_dir = "./generated_pdfs"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_pdf(self, meal_plan: str, patient_name: str, plan_type: str) -> str:
        """Generate PDF from meal plan text"""
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', patient_name)
        filename = f"plan_{plan_type}_{safe_name}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Container for the 'Flowable' objects
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        # Add title
        story.append(Paragraph("PLAN NUTRICIONAL", title_style))
        story.append(Paragraph("Método Tres Días y Carga", subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Add patient info
        story.append(Paragraph(f"<b>Paciente:</b> {patient_name}", body_style))
        story.append(Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}", body_style))
        story.append(Paragraph(f"<b>Tipo de Plan:</b> {plan_type.capitalize()}", body_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Process meal plan text
        lines = meal_plan.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.2*inch))
                continue
            
            # Detect headings
            if any(keyword in line.upper() for keyword in ['DESAYUNO', 'ALMUERZO', 'MERIENDA', 'CENA', 'COLACIÓN']):
                story.append(Paragraph(line, heading_style))
            elif 'RESUMEN NUTRICIONAL' in line.upper():
                story.append(PageBreak())
                story.append(Paragraph(line, title_style))
            elif 'RECOMENDACIONES' in line.upper():
                story.append(Paragraph(line, subtitle_style))
            elif line.startswith('-') or line.startswith('*'):
                # Bullet points
                story.append(Paragraph(f"• {line[1:].strip()}", body_style))
            else:
                # Regular text
                story.append(Paragraph(line, body_style))
        
        # Add footer
        story.append(Spacer(1, inch))
        story.append(Paragraph(
            "Este plan nutricional es personalizado y no debe ser compartido con otras personas.",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        ))
        
        # Build PDF
        doc.build(story)
        
        return filename