from flask import Flask, redirect,render_template, request,flash, url_for
from smtplib import SMTP_SSL
import os
from dotenv import load_dotenv
load_dotenv()


app=Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index_page():
    return render_template("index.html")

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact-me',methods=['GET','POST'])
def contact_page():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')

        with SMTP_SSL("smtp.gmail.com") as connection:
            # connection.starttls()
            connection.login(
                    user=os.environ.get("SENDING_EMAIL"),
                    password=os.environ.get("SENDING_EMAIL_PASSWORD"),
                )
            connection.sendmail(
                from_addr=os.environ.get("SENDING_EMAIL"),
                to_addrs=os.environ.get("RECEIVING_EMAIL"),
                msg=f"Subject:Message from SternleyBlog"
                f"\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}",
                )
            flash('Your message was sent successfully')
        return redirect(url_for('contact_page'))
    return render_template('contact.html')




if __name__=="__main__":
    app.run(debug=True)