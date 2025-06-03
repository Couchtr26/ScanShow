from flask import Flask, render_template, request, send_file
import qrcode
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    video_url = request.form['video_url']
    title = request.form['title']
    notes = request.form['notes']

    qr_img = qrcode.make(video_url)
    img_path = f"generated_qrs/{title.replace(' ', '_')}_qr.png"
    qr_img.save(img_path)

    pdf_path = f"generated_qrs/{title.replace(' ', '_')}_flyer.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, f"ScanShow Flyer: {title}")

    c.drawImage(img_path, width / 2 - 100, height - 350, width=200, height=200)

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 400, "Notes:")
    text_object = c.beginText(50, height - 420)
    lines = notes.splitlines() if notes else ["No additional notes."]
    for line in lines:
        text_object.textLine(line)
    c.drawText(text_object)

    c.save()

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('generated_qrs', exist_ok=True)
    app.run(debug=True)