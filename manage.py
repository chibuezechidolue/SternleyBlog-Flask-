from sqlite3 import IntegrityError
from flask import redirect,render_template, request,flash, url_for
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from forms import CommentForm, CreatePostForm, RegisterUserForm,LoginUserForm,CheckEmailForm, ResetPasswordForm
from werkzeug.security import check_password_hash,generate_password_hash
import datetime
from flask_login import current_user, login_required,login_user,LoginManager,logout_user
from main import app,confirm_token,generate_confirmation_token,logout_required,send_email
from models import BlogPost, Comment, User, UserProfile,db
import datetime





# from flask_script import Manager
load_dotenv()


# app = Manager(app)
# @app.command




# ///////// profile page functionalities/////
@app.route('/profile-page')
def profile_page():
    return render_template('user/profile.html')

# ///////// end profile page functionalities/////



# /////////// CRUD functionality for Posts//////////
@app.route('/confirm-delete/<post_id>',methods=["POST","GET"])
@login_required
def delete_post(post_id):
    post=BlogPost.query.filter_by(id=post_id).first()
    if current_user==post.author:
        if request.method=="POST":
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('index_page'))
    else:
        return "You are not Permitted",403
        
    return render_template("blog/confirm_delete.html",post_id=post_id)


@app.route("/view-post/<post_id>",methods=["GET","POST"])
def view_post(post_id):
    post=BlogPost.query.filter_by(id=post_id).first()
    form=CommentForm()
    # all_comment=db.session.query(Comment).all()
    if request.method=="POST" and form.validate_on_submit:
        text=form.comment.data
        comment=Comment(text=text,post_id=post_id,author=current_user)
        with app.app_context():
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('view_post',post_id=post_id))
    return render_template('blog/post.html',post=post,form=form)



@app.route('/edit-post/<post_id>',methods=["POST","GET"])
@login_required
def edit_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    form=CreatePostForm(title=post.title,subtitle=post.subtitle,img_url=post.img_url,content=post.content)
    if request.method=='POST':
        if form.validate_on_submit:
            post.title=form.title.data
            post.subtitle=form.subtitle.data
            post.img_url=form.img_url.data
            post.content=form.content.data
            db.session.commit()
            return redirect(url_for('index_page'))

    return render_template("blog/make_post.html",form=form,is_edit=True)


@app.route('/create-post',methods=["POST","GET"])
def create_post():
    form=CreatePostForm()
    if request.method=="POST":
        if form.validate_on_submit():
            new_post=BlogPost(title=form.title.data,subtitle=form.subtitle.data,img_url=form.img_url.data,
                              content=form.content.data,date=datetime.date.today(),
                              author_id=current_user.id)
            with app.app_context():
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('index_page'))
    return render_template('blog/make_post.html',form=form)
# /////////// end of CRUD functionality for Posts//////////



# ////////// Reset Password functionality//////
@app.route('/reset-password',methods=['POST','GET'])
def reset_password():
    form=CheckEmailForm()
    if request.method=="POST":
        if form.validate_on_submit():
            email=form.email.data
            if User.query.filter_by(email=email).first():
                token = generate_confirmation_token(email)

                confirm_url = url_for('choose_password', token=token, _external=True)
                html = render_template('user/password_link.html', confirm_url=confirm_url)
                subject = "Reset your password"
                send_email(to=email, subject=subject, template=html)
                return render_template("user/password_reset_done.html")


    return render_template("user/reset_password.html",form=form)
@app.route('/reset-confirm/<token>',methods=["POST","GET"])
def choose_password(token):
    form=ResetPasswordForm()
    try:
        email=confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('reset_password'))
    if request.method=="POST":
        user=User.query.filter_by(email=email).first()
        password=form.password.data
        confirm_pass=form.confirm_pass.data
        if password==confirm_pass:
            print('the password is a match')
            user.password=generate_password_hash(password=password,method=os.environ.get('SECURITY_PASSWORD_SALT'),
                                               salt_length=int(os.environ.get('SALT_ROUNDS')))
            db.session.commit()
            flash('Your password has been reset.', 'success')
            return redirect(url_for('login_page'))
        flash("passwords did not match",'danger')
    return render_template("user/password_reset_confirm.html",form=form)

# ////////// end of Reset Password functionality//////



#/////// login and logout user functionality////////
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
                    login_user(user)
                    
                    return redirect(url_for('index_page'))
            except:
                flash("wrong email, plese try another","danger")
            flash("your password is not correct ","danger")
            
                
    return render_template("user/login.html",form=form)
#/////// end of login and logout user functionality////////


#/////// register user functionality////////
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
                new_user_profile=UserProfile(user=new_user)
                with app.app_context():
                    db.session.add(new_user)
                    db.session.commit()
                    db.session.add(new_user_profile)
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



@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
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


@app.route('/signup-success')
def signup_success_page():
    return render_template('user/signup_success.html')

#/////// end of register user functionality////////


@app.route('/')
def index_page():
    posts = db.session.query(BlogPost).all()
    return render_template("blog/index.html",all_post=posts)

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

