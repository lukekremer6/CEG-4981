import os
import random
import datetime
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'REBEL_ALLIANCE_TOP_SECRET_KEY'

SMTP_CONFIG = {
    "SERVER": "smtp.gmail.com",
    "PORT": 587,
    "SENDER_EMAIL": "khiemdoba03@gmail.com",
    "SENDER_PASSWORD": "igly mflx jmjy hxaq"
}

ALLOWED_USERS = ["khiemdoba03@gmail.com", "do.21@wright.edu"]

verification_codes = {}

def send_email(to_email, code):

    msg = MIMEText(f"Your Rebel Alliance Access Code is: {code}")
    msg['Subject'] = "Rebel Alliance Verification Code"
    msg['From'] = SMTP_CONFIG["SENDER_EMAIL"]
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(SMTP_CONFIG['SERVER'], SMTP_CONFIG['PORT'])
        server.starttls()
        server.login(SMTP_CONFIG["SENDER_EMAIL"], SMTP_CONFIG["SENDER_PASSWORD"])
        server.sendmail(SMTP_CONFIG["SENDER_EMAIL"], [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cropped_images/<path:filename>')
def serve_cropped_image(filename):
    images_dir = os.path.join(os.path.dirname(__file__), '..', 'cropped_images')
    images_dir = os.path.abspath(images_dir)
    from flask import send_from_directory
    return send_from_directory(images_dir, filename)

@app.route('/videos/<path:filename>')
def serve_video(filename):
    videos_dir = os.path.join(os.path.dirname(__file__), '..')
    videos_dir = os.path.abspath(videos_dir)
    from flask import send_from_directory
    return send_from_directory(videos_dir, filename)

@app.route('/api/images')
def get_images():
    images_dir = os.path.join(os.path.dirname(__file__), '..', 'cropped_images')
    images_dir = os.path.abspath(images_dir)
    
    if not os.path.exists(images_dir):
        return jsonify([])
    
    images = []
    for idx, filename in enumerate(os.listdir(images_dir)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append({
                "id": idx + 1,
                "src": f"/cropped_images/{filename}",
                "name": filename.replace('cropped_', '').replace('_', ' ').split('.')[0]
            })
    
    return jsonify(images)

@app.route('/api/login/request-code', methods=['POST'])
def request_code():
    data = request.json
    email = data.get('email', '').strip().lower()

    if email not in ALLOWED_USERS:
        return jsonify({"success": False, "message": "Access Denied: Email not authorized."}), 403

    code = str(random.randint(100000, 999999))
    expires = datetime.datetime.now() + datetime.timedelta(minutes=5)
    
    verification_codes[email] = {
        "code": code,
        "expires": expires
    }

    if send_email(email, code):
        return jsonify({"success": True, "message": "Code sent."})
    else:
        return jsonify({"success": False, "message": "Failed to send email. Check server logs."}), 500

@app.route('/api/login/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()

    record = verification_codes.get(email)

    if not record:
        return jsonify({"success": False, "message": "No code requested."}), 400
    
    if datetime.datetime.now() > record['expires']:
        return jsonify({"success": False, "message": "Code expired."}), 400
    
    if record['code'] == code:
        session['user'] = email
        return jsonify({"success": True, "message": "Authenticated."})
    
    return jsonify({"success": False, "message": "Invalid code."}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
