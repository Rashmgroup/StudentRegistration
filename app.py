from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
import random
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rashmgroup@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_email_password'   # Replace with your email's app password
app.config['MAIL_DEFAULT_SENDER'] = 'rashmgroup@gmail.com'

mail = Mail(app)

# Routes
@app.route("/", methods=["GET", "POST"])
def registration_form():
    if request.method == "POST":
        # Form data
        full_name = request.form.get("Name")
        father_name = request.form.get("Fname")
        email = request.form.get("Email")
        address = request.form.get("Address")
        city = request.form.get("City")
        state = request.form.get("State")
        phone = request.form.get("Phone")
        whatsapp = request.form.get("Whatsapp")
        guardian_phone = request.form.get("GuardianPhone")
        highschool = request.form.get("highschool")
        inter = request.form.get("inter")
        graduation = request.form.get("Graduation")
        course = request.form.get("Course")
        gender = request.form.get("Gender")
        signature = request.form.get("Sign")

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save OTP and email in session
        session['otp'] = otp
        session['email'] = email
        session['registration_data'] = {
            'full_name': full_name,
            'father_name': father_name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'phone': phone,
            'whatsapp': whatsapp,
            'guardian_phone': guardian_phone,
            'highschool': highschool,
            'inter': inter,
            'graduation': graduation,
            'course': course,
            'gender': gender,
            'signature': signature
        }

        # Send OTP email
        try:
            msg = Message("Your OTP Code", recipients=[email])
            msg.body = f"Your OTP code is: {otp}"
            mail.send(msg)
            flash("OTP has been sent to your email address. Please check your inbox.", "info")
            return redirect(url_for("validate_otp"))
        except Exception as e:
            flash(f"Error sending email: {e}", "danger")

    return render_template("registration.html")


@app.route("/validate-otp", methods=["GET", "POST"])
def validate_otp():
    if request.method == "POST":
        # Retrieve user input OTP and session OTP
        user_otp = request.form.get("otp")
        session_otp = session.get("otp")

        if session_otp and str(session_otp) == user_otp:
            # If OTP matches, proceed to complete registration
            registration_data = session.get('registration_data')

            # Generate registration number
            registration_number = f"2024-{random.randint(100000, 999999)}"

            # Email content
            email_body = f"""
            Registration Successful!
            
            Name: {registration_data['full_name']}
            Father's Name: {registration_data['father_name']}
            Email: {registration_data['email']}
            Address: {registration_data['address']}, {registration_data['city']}, {registration_data['state']}
            Phone: {registration_data['phone']}
            WhatsApp: {registration_data['whatsapp']}
            Guardian Phone: {registration_data['guardian_phone']}
            High School: {registration_data['highschool']}
            Intermediate: {registration_data['inter']}
            Graduation: {registration_data['graduation']}
            Course Applied: {registration_data['course']}
            Gender: {registration_data['gender']}
            Signature: {registration_data['signature']}
            Registration Number: {registration_number}
            """

            try:
                # Send registration confirmation email to user
                msg = Message("Registration Confirmation", recipients=[registration_data['email']])
                msg.body = email_body
                mail.send(msg)
                flash(f"Registration successful! A confirmation email has been sent to {registration_data['email']}.", "success")

                # Send a copy of the registration to admin
                msg = Message("New Student Registration", recipients=["rashmgroup@gmail.com"])  # Admin email
                msg.body = email_body
                mail.send(msg)
            except Exception as e:
                flash(f"Error sending confirmation email: {e}", "danger")

            # Clear session OTP and registration data after successful registration
            session.pop('otp', None)
            session.pop('registration_data', None)

            return redirect(url_for("registration_form"))
        else:
            flash("Invalid OTP. Please try again.", "danger")

    return render_template("validate_otp.html")


if __name__ == "__main__":
    app.run(debug=True)
