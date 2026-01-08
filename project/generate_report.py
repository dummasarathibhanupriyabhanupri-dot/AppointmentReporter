import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appointments_db"
)
cursor = conn.cursor()

# Fetch data
cursor.execute("""
SELECT doctor_name, patient_name, appointment_date
FROM appointments
LIMIT 20
""")

rows = cursor.fetchall()

# Create PDF
pdf = canvas.Canvas("appointments_report.pdf", pagesize=A4)
width, height = A4

y = height - 50
pdf.setFont("Helvetica", 12)
pdf.drawString(50, y, "Appointments Report")
y -= 30

pdf.setFont("Helvetica", 10)

for row in rows:
    line = f"Doctor: {row[0]} | Patient: {row[1]} | Date: {row[2]}"
    pdf.drawString(50, y, line)
    y -= 20

    if y < 50:
        pdf.showPage()
        y = height - 50

pdf.save()

cursor.close()
conn.close()

print("✅ PDF report generated successfully")

