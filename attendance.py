import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    name TEXT,
    status TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()


# ---------------- MARK ATTENDANCE ----------------
def mark_attendance(status):
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()

    if not student_id or not name:
        messagebox.showwarning(
            "Warning",
            "Please enter Student ID and Name"
        )
        return

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute("""
        INSERT INTO attendance
        (student_id, name, status, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (student_id, name, status, date, time))

    conn.commit()

    messagebox.showinfo(
        "Success",
        f"{name} marked {status}"
    )

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    show_records()


# ---------------- SHOW RECORDS ----------------
def show_records():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)


# ---------------- SEARCH ----------------
def search_student():
    student_id = search_entry.get().strip()

    if not student_id:
        show_records()
        return

    for item in table.get_children():
        table.delete(item)

    cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id = ?
        ORDER BY id DESC
    """, (student_id,))

    records = cursor.fetchall()

    if not records:
        messagebox.showinfo(
            "Search",
            "No attendance records found"
        )
        return

    for record in records:
        table.insert("", tk.END, values=record)


# ---------------- SUMMARY ----------------
def show_summary():
    student_id = summary_entry.get().strip()

    if not student_id:
        messagebox.showwarning(
            "Warning",
            "Enter Student ID"
        )
        return

    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ?
    """, (student_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ? AND status = 'Present'
    """, (student_id,))

    present = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ? AND status = 'Absent'
    """, (student_id,))

    absent = cursor.fetchone()[0]

    if total == 0:
        messagebox.showinfo(
            "Summary",
            "No attendance records found"
        )
        return

    percentage = (present / total) * 100

    messagebox.showinfo(
        "Attendance Summary",
        f"Student ID: {student_id}\n\n"
        f"Total Classes: {total}\n"
        f"Present: {present}\n"
        f"Absent: {absent}\n"
        f"Attendance Percentage: {percentage:.2f}%"
    )


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Smart Attendance Management System")
root.geometry("950x650")

title = tk.Label(
    root,
    text="Smart Attendance Management System",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)


# ---------------- INPUT SECTION ----------------
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

tk.Label(
    input_frame,
    text="Student ID:",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=8)

id_entry = tk.Entry(
    input_frame,
    width=25
)
id_entry.grid(row=0, column=1, padx=10)


tk.Label(
    input_frame,
    text="Student Name:",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=8)

name_entry = tk.Entry(
    input_frame,
    width=25
)
name_entry.grid(row=1, column=1, padx=10)


# ---------------- ATTENDANCE BUTTONS ----------------
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Present",
    width=15,
    command=lambda: mark_attendance("Present")
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame,
    text="Absent",
    width=15,
    command=lambda: mark_attendance("Absent")
).grid(row=0, column=1, padx=8)

tk.Button(
    button_frame,
    text="Refresh",
    width=15,
    command=show_records
).grid(row=0, column=2, padx=8)


# ---------------- SEARCH SECTION ----------------
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search Student ID:",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5)

search_entry = tk.Entry(
    search_frame,
    width=20
)
search_entry.grid(row=0, column=1, padx=5)

tk.Button(
    search_frame,
    text="Search",
    width=12,
    command=search_student
).grid(row=0, column=2, padx=5)


# ---------------- SUMMARY SECTION ----------------
summary_frame = tk.Frame(root)
summary_frame.pack(pady=5)

tk.Label(
    summary_frame,
    text="Student ID for Summary:",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5)

summary_entry = tk.Entry(
    summary_frame,
    width=20
)
summary_entry.grid(row=0, column=1, padx=5)

tk.Button(
    summary_frame,
    text="View Summary",
    width=15,
    command=show_summary
).grid(row=0, column=2, padx=5)


# ---------------- TABLE ----------------
columns = (
    "ID",
    "Student ID",
    "Name",
    "Status",
    "Date",
    "Time"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=140)

table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)


# ---------------- START ----------------
show_records()

root.mainloop()