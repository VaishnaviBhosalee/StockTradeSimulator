from flask import render_template,redirect,request
from create_app import app
from extensions import db
from models.user import User

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == 'POST':
        user_email = request.form['email']
        user_username = request.form['user_name']
        user_password = request.form['pass_word']
        user_fullname = request.form['full_name']
        user_disp_name = request.form['disp_name']

        new_user = User(email = user_email, 
                        username = user_username, 
                        password = user_password, 
                        fullname = user_fullname, 
                        display_name = user_disp_name)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        except:
            return "There was a problem registering you"
        
    return render_template("register.html")