from sqlite3 import IntegrityError
from flask import redirect,render_template, request,flash, url_for
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from forms import RegisterUserForm,LoginUserForm
from werkzeug.security import check_password_hash
import datetime
from flask_login import current_user, login_required,login_user,LoginManager,logout_user
from main import app,confirm_token,generate_confirmation_token,logout_required,send_email
from models import User,db


# from flask_script import Manager
load_dotenv()


# app = Manager(app)
# @app.command


# to enable login feature
login_manager = LoginManager()
login_manager.init_app(app)

# to loader the logged in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route("/logout")
def logout_page():
    logout_user()
    return render_template('user/logout.html')

@app.route('/login',methods=['POST','GET'])
def login_page():
    form=LoginUserForm()
    if request.method=="POST":
        if form.validate_on_submit:
            email=form.email.data
            password=form.password.data
            try:
                user=User.query.filter_by(email=email).first()
                if check_password_hash(pwhash=user.password,password=password):
                    login_user(user,duration=180)
                    return redirect(url_for('index_page'))
            except:
                flash("wrong email, plese try another","danger")
            flash("your password is not correct ","danger")
            
                
    return render_template("user/login.html",form=form)



@app.route('/register-user',methods=["GET","POST"])
def register_page():
    form=RegisterUserForm()
    if request.method=="POST":
        if form.validate_on_submit():
            username=request.form.get('username')
            if User.query.filter_by(username=username).first():
                flash(message="This username is already taken. Try another",category="danger")       
                # return redirect(url_for('register_page'))
            email=request.form.get('email')
            if User.query.filter_by(email=email).first():
                flash(message="This email already belongs to a user",category="danger")       
                # return redirect(url_for('register_page'))
            phone=request.form.get('phone')
            first_name=request.form.get('first_name')
            last_name=request.form.get('last_name')
            password=request.form.get('password')
            confirm_password=request.form.get('confirm_password')
            if password!=confirm_password:
                flash(message="The passwords did not match",category="danger")
            else:
                accepted_password=password
        

            try:
                new_user=User(username=username,email=email,phone=phone,first_name=first_name,
                          last_name=last_name,password=accepted_password,confirmed=False)
                with app.app_context():
                    db.session.add(new_user)
                    db.session.commit()
                    token = generate_confirmation_token(new_user.email)

                    confirm_url = url_for('confirm_email', token=token, _external=True)
                    html = render_template('user/activate.html', confirm_url=confirm_url)
                    subject = "Please confirm your email"
                    send_email(to=new_user.email, subject=subject, template=html)

                    # login_user(user)

                    flash('A confirmation email has been sent via email.', 'success')
                return redirect(url_for('signup_success_page'))
            except IntegrityError and UnboundLocalError:
                pass

    return render_template('user/register.html',form=form)


@app.route('/signup-success')
def signup_success_page():
    return render_template('user/signup-success.html')



@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    print(email)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        print('user has been confirmed')
        user.confirmed_on = datetime.datetime.now()
        print('user has been confirmed now')
        db.session.commit()

        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('register_page'))



@app.route('/')
def index_page():
    return render_template("blog/index.html")

@app.route('/about')
def about_page():
    return render_template('blog/about.html')

@app.route('/contact-me',methods=['GET','POST'])
def contact_page():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')

        # with SMTP_SSL("smtp.gmail.com") as connection:
        #     # connection.starttls()
        #     connection.login(
        #             user=os.environ.get("SENDING_EMAIL"),
        #             password=os.environ.get("SENDING_EMAIL_PASSWORD"),
        #         )
        #     connection.sendmail(
        #         from_addr=os.environ.get("SENDING_EMAIL"),
        #         to_addrs=os.environ.get("RECEIVING_EMAIL"),
        #         msg=f"Subject:Message from SternleyBlog"
        #         f"\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}",
        #         )
        msg=f"\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}"
        send_email(to=os.environ.get("RECEIVING_EMAIL"),body=msg,subject="Message from SternleyBlog")
        flash('Your message was sent successfully', 'success')
        return redirect(url_for('contact_page'))
    return render_template('blog/contact.html')




if __name__=="__main__":
    app.run(debug=True)

