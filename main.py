import tkinter as tk
from tkinter import messagebox, scrolledtext
import sys
import threading
import time
import matplotlib.pyplot as plt
import pandas as pd

from covertpdf import run as run_covertpdf
from JDParsing import run as run_jdparsing
from newmatric import run as run_newmatric
from advanced_matching import run as run_matching
from schedular import schedule_interviews
from interviewmail import send_interview_emails

class RedirectText:
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def flush(self):
        pass

def run_step(step_function, description):
    def thread_target():
        try:
            status_var.set(f"⏳ {description}...")
            log_text.insert(tk.END, f"\n=== {description} ===\n")
            root.update_idletasks()
            step_function()
            log_text.insert(tk.END, f" {description} completed successfully.\n\n")
            messagebox.showinfo("Success", f"{description} completed successfully.")
        except Exception as e:
            log_text.insert(tk.END, f" Error in {description}:\n{str(e)}\n\n")
            messagebox.showerror("Error", f"{description} failed:\n{str(e)}")
        finally:
            status_var.set("Idle")

    threading.Thread(target=thread_target).start()

def run_all_steps():
    steps_sequence = [
        (run_covertpdf, "Extracting CVs"),
        (run_jdparsing, "Parsing Job Descriptions"),
        (run_newmatric, "Matching CVs with JDs"),
        (run_matching, "Inserting matched data"),
        (schedule_interviews, "Scheduling interviews"),
        (send_interview_emails, "Sending interview emails")
    ]

    for func, desc in steps_sequence:
        status_var.set(f"⏳ {desc}...")
        log_text.insert(tk.END, f"\n=== {desc} ===\n")
        root.update_idletasks()
        try:
            func()
            log_text.insert(tk.END, f" {desc} completed successfully.\n")
        except Exception as e:
            log_text.insert(tk.END, f" Error in {desc}:\n{str(e)}\n")
            messagebox.showerror("Error", f"{desc} failed:\n{str(e)}")
            break
    status_var.set("✅ All steps completed.")
    messagebox.showinfo("Done", "All steps completed successfully.")

def show_match_chart():
    try:
        df = pd.read_csv("skill_experience_percentile_matching.csv")
        df = df[df["Selected"] == "Yes"]
        df_sorted = df.sort_values("Match_Percentage", ascending=True)

        plt.figure(figsize=(10, 6))
        plt.barh(df_sorted["Candidate_Name"], df_sorted["Match_Percentage"], color="skyblue")
        plt.xlabel("Match Percentage")
        plt.title("AI-based Match Percentages of Selected Candidates")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Visualization Error", f"Could not generate graph:\n{str(e)}")

# Update real-time clock
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=f" {current_time}")
    root.after(1000, update_clock)

# GUI setup
root = tk.Tk()
root.title("GetSelect-AI | Job Application Automation - DuelBot")
root.geometry("620x730")
root.resizable(False, False)

# Header
tk.Label(root, text="GetSelect-AI", font=("Helvetica", 20, "bold"), fg="#2c3e50").pack(pady=10)
tk.Label(root, text="DuelBot by Hrishikesh and Rohit", font=("Helvetica", 10, "italic"), fg="gray").pack()

# Status bar
status_var = tk.StringVar()
status_var.set("Idle")
status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor='w')
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Logging pane
tk.Label(root, text="Logs:", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
log_text = scrolledtext.ScrolledText(root, height=15, width=75, wrap=tk.WORD)
log_text.pack(padx=10, pady=5)

# Redirect stdout and stderr
sys.stdout = RedirectText(log_text)
sys.stderr = RedirectText(log_text)

# Buttons
tk.Label(root, text="Actions:", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))

steps = [
    ("Step 1: Extract CVs", lambda: run_step(run_covertpdf, "Extracting CVs")),
    ("Step 2: Parse JDs", lambda: run_step(run_jdparsing, "Parsing Job Descriptions")),
    ("Step 3: Match CVs & JDs", lambda: run_step(run_newmatric, "Matching CVs with JDs")),
    ("Step 4: Store in Database", lambda: run_step(run_matching, "Inserting matched data")),
    ("Step 5: Schedule Interviews", lambda: run_step(schedule_interviews, "Scheduling interviews")),
    ("Step 6: Send Emails", lambda: run_step(send_interview_emails, "Sending interview emails"))
]

for text, command in steps:
    tk.Button(root, text=text, width=50, command=command).pack(pady=3)

# Run All button
tk.Button(root, text="▶ Run All Steps", width=50, bg="#28a745", fg="white",
          command=lambda: threading.Thread(target=run_all_steps).start()).pack(pady=6)

# Show Visualization
tk.Button(root, text=" Show Match % Visualization", width=50, bg="#007bff", fg="white",
          command=show_match_chart).pack(pady=6)

# Real-time Clock Display
clock_label = tk.Label(root, font=("Helvetica", 12), fg="black")
clock_label.pack(pady=(5, 10))
update_clock()

# Run GUI
root.mainloop()
