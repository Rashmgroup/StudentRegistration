from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
import random
import os

app = Flask(__name__)
app.secret_key = "aryanmaurya01"

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rashmgroup@gmail.com'
app.config['MAIL_PASSWORD'] = 'cgyj wqby pxen nged'  # Replace with your app-specific password
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
        OtherCourse = request.form.get("OtherCourse") if course == "Other" else None  # Get the OtherCourse value only if "Other" is selected

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
            'OtherCourse': OtherCourse,  # Save the OtherCourse value
            'gender': gender,
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

            # Email content (HTML)
            # email_body = f"""
            # <html>
            #   <body>
            #     <h1>Registration Successful!</h1>
            #     <p><strong>Name:</strong> {registration_data['full_name']}</p>
            #     <p><strong>Father's Name:</strong> {registration_data['father_name']}</p>
            #     <p><strong>Email:</strong> {registration_data['email']}</p>
            #     <p><strong>Address:</strong> {registration_data['address']}, {registration_data['city']}, {registration_data['state']}</p>
            #     <p><strong>Phone:</strong> {registration_data['phone']}</p>
            #     <p><strong>WhatsApp:</strong> {registration_data['whatsapp']}</p>
            #     <p><strong>Guardian Phone:</strong> {registration_data['guardian_phone']}</p>
            #     <p><strong>High School:</strong> {registration_data['highschool']}</p>
            #     <p><strong>Intermediate:</strong> {registration_data['inter']}</p>
            #     <p><strong>Graduation:</strong> {registration_data['graduation']}</p>
            #     <p><strong>Course Applied:</strong> {registration_data['course']}</p>
            #     {"<p><strong>Other Course:</strong> " + registration_data['OtherCourse'] + "</p>" if registration_data['OtherCourse'] else ""}
            #     <p><strong>Gender:</strong> {registration_data['gender']}</p>
            #     <p><strong>Registration Number:</strong> {registration_number}</p>
            #   </body>
            # </html>
            # """
            email_body = f"""
            <html>
            <head>
                <style>
                /* Basic Email Styling */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f8ff;
                    margin: 0;
                    padding: 0;
                }}
                
                .container {{
                    background-color: white;
                    width: 80%;
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 30px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }}

                h1 {{
                    color: #4CAF50;
                    text-align: center;
                }}
                
                h2 {{
                    color: #198dec;
                    text-align: center;
                }}

                p {{
                    font-size: 1.1em;
                    margin: 10px 0;
                    color: #333;
                }}

                strong {{
                    color: #4CAF50;
                }}
                
                    .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #888;
                }}
                
                /* Responsive Design */
                @media (max-width: 600px) {{
                    h1 {{
                    font-size: 2em;
                    }}
                    p {{
                    font-size: 1em;
                    }}
                }}
                </style>
            </head>
            <body>
                <div class="container">
                <h1>Registration Successful!</h1>
                <h2>Rashm Roadmap Foundation!</h2>
                <p><strong>Name:</strong> {registration_data['full_name']}</p>
                <p><strong>Father's Name:</strong> {registration_data['father_name']}</p>
                <p><strong>Email:</strong> {registration_data['email']}</p>
                <p><strong>Address:</strong> {registration_data['address']}, {registration_data['city']}, {registration_data['state']}</p>
                <p><strong>Phone:</strong> {registration_data['phone']}</p>
                <p><strong>WhatsApp:</strong> {registration_data['whatsapp']}</p>
                <p><strong>Guardian Phone:</strong> {registration_data['guardian_phone']}</p>
                <p><strong>High School:</strong> {registration_data['highschool']}</p>
                <p><strong>Intermediate:</strong> {registration_data['inter']}</p>
                <p><strong>Graduation:</strong> {registration_data['graduation']}</p>
                <p><strong>Course Applied:</strong> {registration_data['course']}</p>
                {f"<p><strong>Other Course:</strong> {registration_data['OtherCourse']}</p>" if registration_data['OtherCourse'] else ""}
                <p><strong>Gender:</strong> {registration_data['gender']}</p>
                <p><strong>Registration Number:</strong> {registration_number}</p>
                <br>
                <div class="footer">
                    <p>Thank you for registering with us!</p>
                    <br>
                    <p>Copyright © All rights reserved | This template is made with ❤ by Aryan Maurya</p>
                </div>
                </div>
            </body>
            </html>
            """

            try:
                # Send registration confirmation email to user
                msg = Message("Registration Confirmation", recipients=[registration_data['email']])
                msg.html = email_body  # Use HTML format for the message
                mail.send(msg)
                flash(f"Registration successful! A confirmation email has been sent to {registration_data['email']}.", "success")

                # Send a copy of the registration to admin
                msg = Message("New Student Registration", recipients=["rashmgroup@gmail.com"])  # Admin email
                msg.html = email_body  # Send email to admin with HTML content
                mail.send(msg)
            except Exception as e:
                flash(f"Error sending confirmation email: {e}", "danger")

            # Clear session OTP and registration data after successful registration
            session.pop('otp', None)
            session.pop('registration_data', None)

            return redirect(url_for("thank_you"))  # Redirect to Thank You page
        else:
            flash("Invalid OTP. Please try again.", "danger")

    return render_template("validate_otp.html")


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


if __name__ == "__main__":
    app.run(debug=True)
