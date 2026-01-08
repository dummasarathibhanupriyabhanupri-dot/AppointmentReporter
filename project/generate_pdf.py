import mysql.connector
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# PDF setup
pdf_file = "therapist_sessions_report.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)

elements = []
styles = getSampleStyleSheet()
elements.append(Paragraph("Therapist Sessions Report", styles['Title']))

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appointments_db"
)
cursor = conn.cursor()

# IMPORTANT QUERY (SUMMARY)
cursor.execute("""
SELECT doctor_name, COUNT(*) AS sessions
FROM appointments
GROUP BY doctor_name
ORDER BY sessions DESC
""")

rows = cursor.fetchall()

# Table header
data = [
    ["Therapist", "Sessions"]
]

# Table rows
for row in rows:
    data.append([
        row[0] if row[0] else "",
        row[1]
    ])

# Create table
table = Table(data, colWidths=[300, 150])

table.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
    ('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 8),
]))

elements.append(table)

doc.build(elements)

cursor.close()
conn.close()

print("✅ Therapist-wise sessions PDF generated")

