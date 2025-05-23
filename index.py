import os
from flask import Flask,render_template,session,request,redirect,url_for
import firebase_admin
from firebase_admin import credentials, firestore
from flask_mail import Mail, Message
from dotenv import load_dotenv
import random
import string
import base64
import json


load_dotenv()


firebase_key_base64 = os.environ.get("BASE64_JSON_FILE")
# print(str(os.environ.get("BASE64_JSON_FILE")))

firebase_key_json = base64.b64decode(firebase_key_base64).decode("utf-8")
firebase_key_dict = json.loads(firebase_key_json)

cred = credentials.Certificate(firebase_key_dict)
# print("#################################################")
# print(cred)
firebase_admin.initialize_app(cred)

db = firestore.client()

app= Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'programmingsir999@gmail.com'      # Replace with your email
app.config['MAIL_PASSWORD'] = 'gxkzdrtpoasutbns'        # Replace with your email password or app password

mail = Mail(app)

@app.route('/')
def res_homepage():
    # print(os.environ.get("FIREBASE_KEY_PATH"))  # Example: print the FIREBASE_KEY_PATH environment variable
    # print( "chack2"+str(os.environ.get("BASE64_JSON_FILE")))
    return render_template('add_admin.html')

@app.route('/add_adminlogin', methods=["GET", "POST"])
def add_adminlogin():
    admins_ref = db.collection('admins').get()
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        # Generate random password
        # In your route:
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Delete all previous admin records
        admins_ref = db.collection('admins').get()
        for doc in admins_ref:
            db.collection('admins').document(doc.id).delete()

        
        # Store in Firestore
        db.collection('admins').add({
            'name': name,
            'email': email,
            'password': password
        })
        # Send email
        msg = Message(
            'Official Notification: Admin Account Created',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = (
            f"Dear {name},\n\n"
            "We are pleased to inform you that your administrator account has been successfully created.\n\n"
            f"Your login credentials are as follows:\n"
            f"Email: {email}\n"
            f"Password: ***{password}***\n\n"
            "Please keep this information confidential and do not share it with anyone.\n\n"
            "If you have any questions or require assistance, please contact the IT department.\n\n"
            "Regards,\n"
            "Government Administration Team"
        )
        mail.send(msg)
        return render_template('add_successful.html', name=name, email=email, password=password)
    return render_template('add_adminlogin.html')

if __name__=="__main__":
    app.run(debug=True, port=3005)