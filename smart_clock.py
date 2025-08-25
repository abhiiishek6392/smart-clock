import tkinter as tk
from tkinter import messagebox
import time
import threading
import datetime
import pytz
import winsound   # works on Windows for alarm sound

class SmartClock:
    def __init__(self, root):

        self.root = root
        self.root.title("Smart Multi-Feature Clock")
        self.root.geometry("400x500")
        
        # ---------------- Digital Clock ----------------
        self.time_label = tk.Label(root, font=("Arial", 24), fg="black")
        self.time_label.pack(pady=10)
        self.update_time()

        # ---------------- Alarm ----------------
        tk.Label(root, text="Set Alarm (HH:MM:SS)", font=("Arial", 12)).pack()
        self.alarm_entry = tk.Entry(root, font=("Arial", 12))
        self.alarm_entry.pack()
        tk.Button(root, text="Set Alarm", command=self.set_alarm).pack(pady=5)

        # ---------------- Stopwatch ----------------
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.stopwatch_label = tk.Label(root, text="00:00:00", font=("Arial", 20))
        self.stopwatch_label.pack(pady=10)
        tk.Button(root, text="Start Stopwatch", command=self.start_stopwatch).pack()
        tk.Button(root, text="Stop Stopwatch", command=self.stop_stopwatch).pack()
        tk.Button(root, text="Reset Stopwatch", command=self.reset_stopwatch).pack()

        # ---------------- Countdown Timer ----------------
        tk.Label(root, text="Countdown (seconds)", font=("Arial", 12)).pack()
        self.timer_entry = tk.Entry(root, font=("Arial", 12))
        self.timer_entry.pack()
        tk.Button(root, text="Start Countdown", command=self.start_countdown).pack(pady=5)
        self.timer_label = tk.Label(root, text="", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        # ---------------- World Clock ----------------
        tk.Label(root, text="World Clock", font=("Arial", 14)).pack(pady=10)
        self.world_label = tk.Label(root, font=("Arial", 12))
        self.world_label.pack()
        self.update_world_clock()

    # ---------------- Digital Clock Function ----------------
    def update_time(self):
        current_time = time.strftime("%H:%M:%S %p\n%d-%m-%Y")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    # ---------------- Alarm Function ----------------
    def set_alarm(self):
        alarm_time = self.alarm_entry.get()
        threading.Thread(target=self.check_alarm, args=(alarm_time,), daemon=True).start()

    def check_alarm(self, alarm_time):
        while True:
            current_time = time.strftime("%H:%M:%S")
            if current_time == alarm_time:
                winsound.Beep(1000, 2000)  # Beep sound for 2 sec
                messagebox.showinfo("Alarm", "Wake up! Alarm time reached!")
                break
            time.sleep(1)

    # ---------------- Stopwatch Functions ----------------
    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            threading.Thread(target=self.run_stopwatch, daemon=True).start()

    def run_stopwatch(self):
        while self.stopwatch_running:
            self.stopwatch_time += 1
            mins, secs = divmod(self.stopwatch_time, 60)
            hrs, mins = divmod(mins, 60)
            self.stopwatch_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
            time.sleep(1)

    def stop_stopwatch(self):
        self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.stopwatch_label.config(text="00:00:00")

    # ---------------- Countdown Timer ----------------
    def start_countdown(self):
        try:
            count = int(self.timer_entry.get())
            threading.Thread(target=self.run_countdown, args=(count,), daemon=True).start()
        except:
            messagebox.showerror("Error", "Enter valid number")

    def run_countdown(self, count):
        while count > 0:
            mins, secs = divmod(count, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            time.sleep(1)
            count -= 1
        self.timer_label.config(text="Time's Up!")
        winsound.Beep(800, 1500)

    # ---------------- World Clock ----------------
    def update_world_clock(self):
        india = datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("India: %H:%M:%S")
        usa = datetime.datetime.now(pytz.timezone("US/Eastern")).strftime("USA: %H:%M:%S")
        london = datetime.datetime.now(pytz.timezone("Europe/London")).strftime("London: %H:%M:%S")
        self.world_label.config(text=f"{india}\n{usa}\n{london}")
        self.root.after(1000, self.update_world_clock)

# ---------------- Run App ----------------
root = tk.Tk()
app = SmartClock(root)
root.mainloop()