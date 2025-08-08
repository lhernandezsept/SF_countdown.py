#!/usr/bin/env python
# coding: utf-8

# In[424]:


import tkinter as tk
import datetime
import pytz
import random

# --- SETUP ---
root = tk.Tk()
root.title("Golden Baes: Countdown to Aug 26, 2025 10 AM")
root.geometry("500x600")
root.configure(bg="#fff8f0")

# --- Fonts & Text ---
script_font = ("Brush Script MT", 24, "bold")
title_font = 16
base_font_size = title_font
heart_icon = "❤️"

# --- Top Label ---
lbl = tk.Label(
    root,
    text="Before the vow, there’s a date — and that’s where time begins",
    font=script_font,
    bg="#fff8f0",
    wraplength=460,
    justify="center"
)
lbl.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="ew")
root.grid_columnconfigure(0, weight=1)

# --- Countdown Label (Hidden initially) ---
countdown_label = tk.Label(root, text="", font=("Helvetica", 18, "bold"), bg="#fff8f0", fg="black")
countdown_label.grid(row=2, column=0, pady=(20, 0))
countdown_label.grid_remove()

# --- Timezone Clocks (Hidden initially) ---
chicago_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#fff8f0", fg="#333")
sf_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), bg="#fff8f0", fg="#ff4500")

chicago_label.grid(row=3, column=0, pady=(10, 0))
sf_label.grid(row=4, column=0, pady=(0, 20))
chicago_label.grid_remove()
sf_label.grid_remove()

# --- Canvas for confetti and hearts (hidden initially) ---
confetti_canvas = tk.Canvas(root, width=500, height=600, bg="#fff8f0", highlightthickness=0)
confetti_canvas.grid(row=0, column=0, rowspan=10)
confetti_canvas.grid_remove()

# --- Target datetime for countdown: Aug 26, 2025, 10:00 AM SF time ---
sf_tz = pytz.timezone("America/Los_Angeles")
target_date_naive = datetime.datetime(2025, 8, 26, 10, 0, 0)
target_date_sf = sf_tz.localize(target_date_naive)

# --- Confetti trigger times ---
confetti_time_9am = sf_tz.localize(datetime.datetime(2025, 8, 26, 9, 0, 0))
confetti_time_10am = target_date_sf

confetti_triggered_9am = False
confetti_triggered_10am = False

# --- Animation & confetti state ---
sf_colors = ["#ff4500", "#ff6347", "#ff7f50", "#ff4500"]
sf_anim_index = 0
confetti_running = False
confetti_items = []

# --- Floating hearts state ---
floating_hearts = []
heart_symbols = ["❤️", "💕", "💖", "💘"]

# --- Functions for confetti ---
def create_confetti():
    confetti_colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#8f00ff"]
    for _ in range(100):
        x = random.randint(10, 490)
        y = random.randint(10, 590)
        size = random.randint(5, 15)
        color = random.choice(confetti_colors)
        item = confetti_canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        confetti_items.append(item)

def clear_confetti():
    for item in confetti_items:
        confetti_canvas.delete(item)
    confetti_items.clear()

def run_confetti(duration=3000):
    global confetti_running
    if confetti_running:
        return
    confetti_running = True
    confetti_canvas.lift()
    confetti_canvas.grid()
    create_confetti()
    root.after(duration, stop_confetti)

def stop_confetti():
    global confetti_running
    clear_confetti()
    confetti_canvas.grid_remove()
    confetti_running = False

# --- Floating hearts functions ---
def create_floating_heart():
    x = random.randint(50, 450)
    y = 580
    size = random.randint(20, 30)
    heart = random.choice(heart_symbols)

    heart_item = confetti_canvas.create_text(
        x, y, text=heart, font=("Arial", size, "bold"), fill="#ff69b4"
    )
    floating_hearts.append((heart_item, 0))

def animate_floating_hearts():
    for heart_item, frame in list(floating_hearts):
        if frame > 60:
            confetti_canvas.delete(heart_item)
            floating_hearts.remove((heart_item, frame))
        else:
            confetti_canvas.move(heart_item, 0, -2)
            index = floating_hearts.index((heart_item, frame))
            floating_hearts[index] = (heart_item, frame + 1)

    root.after(100, animate_floating_hearts)

def start_floating_hearts():
    create_floating_heart()
    root.after(random.randint(800, 1500), start_floating_hearts)

# --- Animate SF label color ---
def animate_sf_label():
    global sf_anim_index
    sf_label.config(fg=sf_colors[sf_anim_index])
    sf_anim_index = (sf_anim_index + 1) % len(sf_colors)
    root.after(500, animate_sf_label)

# --- Update clocks & countdown ---
def update_clocks():
    global confetti_triggered_9am, confetti_triggered_10am
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    chicago_tz = pytz.timezone("America/Chicago")
    now_chicago = now_utc.astimezone(chicago_tz)
    now_sf = now_utc.astimezone(sf_tz)

    delta_chicago = target_date_sf.astimezone(chicago_tz) - now_chicago
    delta_sf = target_date_sf - now_sf

    # Countdown breakdowns
    days_c = max(delta_chicago.days, 0)
    hours_c, remainder_c = divmod(max(delta_chicago.seconds, 0), 3600)
    minutes_c, _ = divmod(remainder_c, 60)

    days_sf = max(delta_sf.days, 0)
    hours_sf, remainder_sf = divmod(max(delta_sf.seconds, 0), 3600)
    minutes_sf, _ = divmod(remainder_sf, 60)
    seconds_sf = max(delta_sf.seconds % 60, 0)

    chicago_time_str = now_chicago.strftime("%I:%M:%S %p")
    sf_time_str = now_sf.strftime("%I:%M:%S %p")

    countdown_c_str = f"{days_c}d {hours_c}h {minutes_c}m left"
    countdown_sf_str = f"{days_sf}d {hours_sf}h {minutes_sf}m {seconds_sf}s left"

    # --- Special timed messages ---
    special_msg = ""
    current_date = now_sf.date()
    current_time = now_sf.time()
    now_sf_floor = now_sf.replace(microsecond=0)

    if current_date == datetime.date(2025, 8, 26):
        if datetime.time(6, 0) <= current_time <= datetime.time(8, 0):
            special_msg = "1850 miles away to moments away ✈️"
        elif current_time.hour == 8 and current_time.minute == 56:
            special_msg = "Landed. 💼❤️"
        elif current_time.hour == 10 and current_time.minute == 0:
            special_msg = "Celebrating love 💍🎉"

    # Confetti triggers at 9AM and 10AM SF time
    if not confetti_triggered_9am and abs((now_sf_floor - confetti_time_9am).total_seconds()) < 1:
        run_confetti()
        confetti_triggered_9am = True
        special_msg = "🎉 It’s 9 AM! 🎉"
    elif not confetti_triggered_10am and abs((now_sf_floor - confetti_time_10am).total_seconds()) < 1:
        run_confetti()
        confetti_triggered_10am = True
        special_msg = "🎉 It’s 10 AM! 🎉"

    # Update UI labels
    chicago_label.config(text=f"🕒 Chicago Time: {chicago_time_str}  |  Countdown: {countdown_c_str}")
    sf_label.config(text=f"🕒 San Francisco Time: {sf_time_str}  |  Countdown: {countdown_sf_str} {special_msg}")

    root.after(1000, update_clocks)

# --- Update countdown (days only) ---
def update_countdown():
    today = datetime.date.today()
    days_left = (target_date_sf.date() - today).days
    countdown_label.config(text=f"💖 {days_left} days until San Francisco 💖")
    root.after(86400000, update_countdown)  # Daily update

# --- Button and heartbeat animation ---
def on_button_click():
    btn.grid_remove()
    confetti_canvas.grid()  # Show canvas for hearts/confetti
    start_floating_hearts()
    animate_floating_hearts()
    root.after(3000, show_countdown_and_clocks)

def show_countdown_and_clocks():
    print("Showing countdown and clocks now!")
    confetti_canvas.grid_remove()  # <-- Hide confetti so countdown/clocks show
    countdown_label.grid()
    chicago_label.grid()
    sf_label.grid()
    update_countdown()
    update_clocks()
    animate_sf_label()

btn = tk.Button(
    root,
    text=f"{heart_icon} Tap here for forever {heart_icon}",
    font=("Helvetica", title_font, "bold"),
    bg="#ffd700",
    fg="black",
    activebackground="#ffb700",
    activeforeground="black",
    relief="flat",
    padx=20,
    pady=10,
    command=on_button_click
)
btn.grid(row=1, column=0, pady=40)

def heartbeat(scale=1.0, growing=True):
    if not btn.winfo_exists():
        return
    new_size = int(base_font_size * scale)
    btn.config(font=("Helvetica", new_size, "bold"))
    if growing and scale < 1.2:
        root.after(80, heartbeat, scale + 0.05, True)
    elif growing:
        root.after(80, heartbeat, scale, False)
    elif scale > 1.0:
        root.after(80, heartbeat, scale - 0.05, False)
    else:
        root.after(800, heartbeat, 1.0, True)

heartbeat()
root.mainloop()


# In[425]:




from flask import Flask, render_template_string
import datetime
import pytz

app = Flask(__name__)

sf_tz = pytz.timezone("America/Los_Angeles")
target_date = sf_tz.localize(datetime.datetime(2025, 8, 26, 10, 0, 0))

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Golden Baes Countdown</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #fff8f0;
      color: #333;
      text-align: center;
      padding: 50px;
    }
    h1 {
      font-family: 'Brush Script MT', cursive;
      font-size: 36px;
      margin-bottom: 20px;
    }
    #countdown {
      font-size: 24px;
      margin: 20px 0;
      font-weight: bold;
      color: #ff4500;
    }
    #message {
      font-size: 20px;
      margin-top: 10px;
      color: #ff6347;
    }
  </style>
</head>
<body>
  <h1>Before the vow, there’s a date — and that’s where time begins</h1>
  <div id="countdown">Loading countdown...</div>
  <div id="message"></div>

<script>
function updateCountdown() {
  // Target time in San Francisco timezone (PDT/PST)
  const target = new Date("{{ target_date_iso }}");

  // Current time (browser local time)
  const now = new Date();

  // Difference in milliseconds
  let diff = target - now;

  if (diff < 0) {
    document.getElementById('countdown').textContent = "💍 The day has arrived! 🎉";
    document.getElementById('message').textContent = "Celebrating love 💖";
    return;
  }

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  diff -= days * (1000 * 60 * 60 * 24);

  const hours = Math.floor(diff / (1000 * 60 * 60));
  diff -= hours * (1000 * 60 * 60);

  const minutes = Math.floor(diff / (1000 * 60));
  diff -= minutes * (1000 * 60);

  const seconds = Math.floor(diff / 1000);

  document.getElementById('countdown').textContent = 
    `💖 ${days}d ${hours}h ${minutes}m ${seconds}s until San Francisco 💖`;

  // Special messages based on current SF time
  const sfNow = new Date(new Date().toLocaleString("en-US", {timeZone: "America/Los_Angeles"}));
  const hoursSF = sfNow.getHours();
  const minutesSF = sfNow.getMinutes();

  let specialMsg = "";
  if (sfNow.getMonth() === 7 && sfNow.getDate() === 26) { // August 26 (0-based month!)
    if (hoursSF >= 6 && hoursSF <= 8) {
      specialMsg = "1850 miles away to moments away ✈️";
    } else if (hoursSF === 8 && minutesSF === 56) {
      specialMsg = "Landed. 💼❤️";
    } else if (hoursSF === 10 && minutesSF === 0) {
      specialMsg = "Celebrating love 💍🎉";
    }
  }
  document.getElementById('message').textContent = specialMsg;

  setTimeout(updateCountdown, 1000);
}

updateCountdown();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    # Pass target date in ISO format for JavaScript
    return render_template_string(HTML, target_date_iso=target_date.isoformat())

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:


import threading
import webview
from flask import Flask, render_template_string
import datetime
import pytz

app = Flask(__name__)

sf_tz = pytz.timezone("America/Los_Angeles")
target_date = sf_tz.localize(datetime.datetime(2025, 8, 26, 10, 0, 0))

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Golden Baes Countdown</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #fff8f0;
      color: #333;
      text-align: center;
      padding: 50px;
    }
    h1 {
      font-family: 'Brush Script MT', cursive;
      font-size: 36px;
      margin-bottom: 20px;
    }
    #countdown {
      font-size: 24px;
      margin: 20px 0;
      font-weight: bold;
      color: #ff4500;
    }
    #message {
      font-size: 20px;
      margin-top: 10px;
      color: #ff6347;
    }
  </style>
</head>
<body>
  <h1>Before the vow, there’s a date — and that’s where time begins</h1>
  <div id="countdown">Loading countdown...</div>
  <div id="message"></div>

<script>
function updateCountdown() {
  const target = new Date("{{ target_date_iso }}");
  const now = new Date();
  let diff = target - now;

  if (diff < 0) {
    document.getElementById('countdown').textContent = "💍 The day has arrived! 🎉";
    document.getElementById('message').textContent = "Celebrating love 💖";
    return;
  }

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  diff -= days * (1000 * 60 * 60 * 24);
  const hours = Math.floor(diff / (1000 * 60 * 60));
  diff -= hours * (1000 * 60 * 60);
  const minutes = Math.floor(diff / (1000 * 60));
  diff -= minutes * (1000 * 60);
  const seconds = Math.floor(diff / 1000);

  document.getElementById('countdown').textContent = 
    `💖 ${days}d ${hours}h ${minutes}m ${seconds}s until San Francisco 💖`;

  const sfNow = new Date(new Date().toLocaleString("en-US", {timeZone: "America/Los_Angeles"}));
  const hoursSF = sfNow.getHours();
  const minutesSF = sfNow.getMinutes();

  let specialMsg = "";
  if (sfNow.getMonth() === 7 && sfNow.getDate() === 26) {
    if (hoursSF >= 6 && hoursSF <= 8) {
      specialMsg = "1850 miles away to moments away ✈️";
    } else if (hoursSF === 8 && minutesSF === 56) {
      specialMsg = "Landed. 💼❤️";
    } else if (hoursSF === 10 && minutesSF === 0) {
      specialMsg = "Celebrating love 💍🎉";
    }
  }
  document.getElementById('message').textContent = specialMsg;

  setTimeout(updateCountdown, 1000);
}

updateCountdown();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, target_date_iso=target_date.isoformat())

def run_flask():
    app.run(threaded=True, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    webview.create_window("Golden Baes Countdown", "http://127.0.0.1:5000")
    webview.start()


# In[ ]:





# In[ ]:




