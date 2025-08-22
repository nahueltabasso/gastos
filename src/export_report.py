from fpdf import FPDF 
from crud import obtener_gastos, obtener_totales, obtener_pagos, obtener_totales_pagos
from models import Gasto
from config import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import smtplib, ssl
import pandas as pd 
import os

class PDFService:
    def __init__(self, data: list[Gasto]):
        """
        Initialize the PDF with a title and the DataFrame to convert into a table.
        :param title: Title for the PDF document.
        :param data: Pandas DataFrame that holds the data to be displayed in the table.
        """
        self.data = data
        self.dataframe = None
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Times", size=16)
        
    def set_data(self): 
        gastos_dict = [d.to_dict() for d in self.data]
        self.dataframe = pd.DataFrame(gastos_dict)
        
    def add_title(self, title):
        """Agrega un titulo al PDF."""
        self.pdf.set_font("Times", style="B", size=18)
        self.pdf.cell(0, 10, title, ln=True, align="C")
        self.pdf.ln(10)

    def add_table(self):
        """Agrega una tabla a partir de un Dataframe a un PDF."""
        # Create the table
        cols = self.dataframe.columns.tolist()
        ncols = len(cols)
        # ancho disponible en la página
        page_width = self.pdf.w - 2 * self.pdf.l_margin

        # Porcentaje para la columna DESCRIPCION (ajustar si se desea)
        desc_pct = 0.40
        desc_width = page_width * desc_pct if 'DESCRIPCION' in cols else page_width / max(ncols, 1)
        # ancho restante repartido entre las demás columnas
        remaining_cols = ncols - (1 if 'DESCRIPCION' in cols else 0)
        other_width = (page_width - desc_width) / max(remaining_cols, 1)

        line_height = 8

        # Header
        self.pdf.set_font("Times", style="B", size=12)
        self.pdf.set_fill_color(200, 200, 200)
        for col in cols:
            w = desc_width if col == 'DESCRIPCION' else other_width
            self.pdf.cell(w, line_height, str(col), border=1, ln=0, align='C', fill=True)
        self.pdf.ln(line_height)

        # Filas (fuente más pequeña)
        self.pdf.set_font("Times", size=10)
        for _, row in self.dataframe.iterrows():
            for col in cols:
                w = desc_width if col == 'DESCRIPCION' else other_width
                item = row.get(col, "") if hasattr(row, "get") else row[cols.index(col)]
                text = "" if pd.isna(item) else str(item)
                # Truncar texto si es muy largo para evitar overflow en la celda
                max_chars = max(10, int(w / 2.5))
                if len(text) > max_chars:
                    text = text[:max_chars-3] + "..."
                self.pdf.cell(w, line_height, text, border=1)
            self.pdf.ln(line_height)

    def save_pdf(self, filename: str):
        """Genera el archivo PDF y lo escribe en el sistema de archivos."""
        try:
            self.pdf.output(filename)
        except Exception as e:
            print(f"Error al guardar el PDF: {e}")
            raise
        
def _add_title(pdf: PDFService, title: str) -> None:
    pdf.add_title(title=title)

def _add_table(pdf: PDFService) -> None:
    pdf.add_table()
    
def _send_email(filename: str='') -> None:
    sender_email = settings.GMAIL_SENDER_MAIL
    receiver_email = settings.GMAIL_RECEIVER_MAIL
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reportes de Gastos y Pagos"
    message["From"] = sender_email
    message["To"] = receiver_email
    html = "<html><body><h1>Reporte</h1></body></html>"
    
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    part1 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part)

    # Create a secure SSL context
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(settings.GMAIL_MAIL_SERVER, settings.GMAIL_MAIL_PORT, context=context) as server:
            server.login(settings.GMAIL_USERNAME, settings.GMAIL_PASSWORD)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except smtplib.SMTPException as e:
        print(f"Error al enviar el email: {e}")
        raise
        
def build_pdf_gastos_report(email_flag: bool=False) -> None:
    try:
        gastos, totales = obtener_gastos(), obtener_totales(tipo='Gastos Casa')
        pdf = PDFService(data=gastos)
        _add_title(pdf, title="Listado de Gastos - Remodelacion Casa")
        pdf.set_data()
        _add_table(pdf)
        _add_title(pdf, title="Totales de Gastos - Remodelacion Casa")
        pdf.dataframe = pd.DataFrame([totales.to_dict()])
        _add_table(pdf)
        filename = "reporte_gastos.pdf"
        pdf.save_pdf(filename=filename)
        print("PDF generado exitosamente: gastos_remodelacion_casa.pdf")
        if email_flag:
            print("Enviando reporte por email...")
            _send_email(filename=filename)
            print("Email enviado exitosamente.")
            os.remove(filename)
    except Exception as e:
        print(f"Error al generar el reporte de gastos: {e}")
            
def build_pdf_pagos_report(email_flag: bool=False) -> None:
    try:
        pagos = obtener_pagos()
        totales = obtener_totales_pagos(pagos=pagos)
        pdf = PDFService(data=pagos)
        _add_title(pdf, title="Listado de Pagos - Casa")
        pdf.set_data()
        _add_table(pdf)
        _add_title(pdf, title="Totales de Pagos - Casa")
        pdf.dataframe = pd.DataFrame([totales.to_dict()])
        _add_table(pdf)
        filename = "reporte_pagos.pdf"
        pdf.save_pdf(filename=filename)
        print("PDF generado exitosamente: reporte_pagos.pdf")
        if email_flag:
            print("Enviando reporte por email...")
            _send_email(filename=filename)
            print("Email enviado exitosamente.")
            os.remove(filename)
    except Exception as e:
        print(f"Error al generar el reporte de pagos: {e}")
    