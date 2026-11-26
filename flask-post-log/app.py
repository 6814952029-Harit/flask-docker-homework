from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "log.txt"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Flask POST Logger</title></head>
<body style="font-family: sans-serif; margin: 40px;">
    <h2>ส่งข้อความบันทึกลงไฟล์ log.txt</h2>
    <form method="POST">
        <input type="text" name="message" placeholder="พิมพ์ข้อความที่นี่..." required style="padding: 8px; width: 250px;">
        <button type="submit" style="padding: 8px 16px;">ส่งข้อมูล (POST)</button>
    </form>
    {% if submitted_msg %}
        <p style="color: green;"><strong>ข้อความล่าสุดที่ได้รับ:</strong> {{ submitted_msg }}</p>
    {% endif %}
    <hr>
    <h3>ประวัติข้อความใน log.txt:</h3>
    <pre style="background: #f4f4f4; padding: 15px;">{{ logs }}</pre>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    submitted_msg = None
    if request.method == "POST":
        submitted_msg = request.form.get("message", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {submitted_msg}\n")

    logs = ""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.read()

    return render_template_string(HTML_TEMPLATE, submitted_msg=submitted_msg, logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)