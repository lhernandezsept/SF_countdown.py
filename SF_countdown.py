Flask==2.2.5
pytz
gunicorn

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

if __name__ == "__main__":
    app.run()
