import pandas as pd
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appointments_db"
)
cursor = conn.cursor()

# Read CSV
df = pd.read_csv("AppointmentsReport (16).csv")

# Rename columns (CSV → DB match)
df = df.rename(columns={
    'Doctor Name': 'doctor_name',
    'Patient Localid': 'patient_localid',
    'Patient Name': 'patient_name',
    'Age': 'age',
    'Gender': 'gender',
    'Email': 'email',
    'Contact': 'contact',
    'City': 'city',
    'Area': 'area',
    'Created At': 'created_at',
    'Appointment Date': 'appointment_date',
    'Duration': 'duration',
    'Cancelled At': 'cancelled_at',
    'Missed': 'missed',
    'Checkin At': 'checkin_at',
    'Engaged At': 'engaged_at',
    'Completed At': 'completed_at',
    'Corporate Name': 'corporate_name',
    'Employee Id': 'employee_id',
    'Relationship': 'relationship',
    'Cowin Reference ID': 'cowin_reference_id',
    'Cowin Registered Name': 'cowin_registered_name',
    'Cowin Registered Mobile': 'cowin_registered_mobile',
    'Vaccine Name': 'vaccine_name',
    'Vaccine Dose': 'vaccine_dose',
    'JHH Patient ID': 'jhh_patient_id'
})

# Date columns convert
date_cols = [
    'created_at','appointment_date','cancelled_at',
    'checkin_at','engaged_at','completed_at'
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

# Replace NaN → None
df = df.astype(object)
df = df.where(pd.notnull(df), None)

# Insert query
sql = """
INSERT INTO appointments (
    doctor_name, patient_localid, patient_name, age, gender, email, contact,
    city, area, created_at, appointment_date, duration, cancelled_at, missed,
    checkin_at, engaged_at, completed_at, corporate_name, employee_id,
    relationship, cowin_reference_id, cowin_registered_name,
    cowin_registered_mobile, vaccine_name, vaccine_dose, jhh_patient_id
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

# Insert rows
for _, row in df.iterrows():
    cursor.execute(sql, (
        row['doctor_name'],
        row['patient_localid'],
        row['patient_name'],
        row['age'],
        row['gender'],
        row['email'],
        row['contact'],
        row['city'],
        row['area'],
        row['created_at'],
        row['appointment_date'],
        row['duration'],
        row['cancelled_at'],
        row['missed'],
        row['checkin_at'],
        row['engaged_at'],
        row['completed_at'],
        row['corporate_name'],
        row['employee_id'],
        row['relationship'],
        row['cowin_reference_id'],
        row['cowin_registered_name'],
        row['cowin_registered_mobile'],
        row['vaccine_name'],
        row['vaccine_dose'],
        row['jhh_patient_id']
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ CSV data inserted into appointments table")
