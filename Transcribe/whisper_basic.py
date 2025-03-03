import whisper
import torch
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Verificar si CUDA está disponible
print("CUDA available:", torch.cuda.is_available())
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")

# Cargar el modelo Whisper
model = whisper.load_model("turbo")
result = model.transcribe("Vision7.mp3", word_timestamps=True)  # Activar marcas de tiempo

# Configurar el PDF con hoja A4
pdf_filename = "Vision_27_02_2025.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)

# Crear estilos de texto (justificado y para los indicadores de minutos)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Justify", alignment=4))  # Justificar el texto
styles.add(ParagraphStyle(name="TimeMarker", fontSize=14, spaceBefore=10, spaceAfter=5, textColor="blue", bold=True))

# Obtener la transcripción con timestamps
segments = result["segments"]

# Organizar el texto en bloques de 5 minutos
content = []
current_time = 0
text_block = ""

for segment in segments:
    start_time = segment["start"]  # Tiempo de inicio en segundos
    text = segment["text"]

    # Si han pasado 5 minutos, agregar un indicador y reiniciar el bloque de texto
    if start_time >= current_time:
        if text_block:
            content.append(Paragraph(text_block, styles["Justify"]))
            content.append(Spacer(1, 12))  # Espaciado entre bloques

        # Agregar marcador de minuto
        minutes = int(current_time // 60)
        content.append(Paragraph(f"🕒 Minuto {minutes}", styles["TimeMarker"]))
        content.append(Spacer(1, 8))

        text_block = ""  # Reiniciar bloque de texto
        current_time += 300  # Avanzar 5 minutos

    text_block += text + " "

# Agregar el último bloque de texto al contenido
if text_block:
    content.append(Paragraph(text_block, styles["Justify"]))

# Generar el PDF
doc.build(content)
print(f"Transcription saved as {pdf_filename}")
