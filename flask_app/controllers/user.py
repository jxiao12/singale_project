from tempfile import tempdir
from turtle import position

from bcrypt import re
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.company import Company
from flask_app.models.position import Position
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



# @app.route('/login_or_register')
# def logins():
#     return render_template("login.html")

# @app.route('/login',methods=['POST'])
# def login():
#     user = User.get_by_email(request.form)

#     if not user:
#         flash("Invalid Email","login")
#         return redirect('/')
#     if not bcrypt.check_password_hash(user.password, request.form['password']):
#         flash("Invalid Password","login")
#         return redirect('/')
#     session['user_id'] = user.id
    
#     return redirect('/')

# @app.route('/register',methods=['POST'])
# def register():
#     if not User.validate_register(request.form):
#         return redirect('/')
#     data ={ 
#         "first_name": request.form['first_name'],
#         "last_name": request.form['last_name'],
#         "email": request.form['email'],
#         "password": bcrypt.generate_password_hash(request.form['password'])
#     }
#     id = User.save(data)
#     session['user_id'] = id

#     return redirect('/')
  

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')

@app.route('/user_main/<int:id>')
def main(id):
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template('person.html',
                            user = User.get_by_id(user_data))



@app.route('/')
def index():
    if 'user_id' in session:
        data ={
            'id': session['user_id']
        }
        if "kind" in session:
            kind_data = {
                "kind": session['kind']
            }
            return render_template('index.html',
                                company = Company.get_all(), 
                                position_kind = Position.get_kind(kind_data),
                                user = User.get_by_id(data)
                                )

        if "place" in session:
            place_data = {
                "place": session['place']
            }
            return render_template('index.html',
                                company = Company.get_all(), 
                                position_place = Position.get_place(place_data),
                                user = User.get_by_id(data)
                                )
        return render_template('index.html',
                                company = Company.get_all(), 
                                positions = Position.get_all(),
                                user = User.get_by_id(data)
                                )
    elif 'company_id' in session:
        data = {
            'id': session['company_id']
        }
        if "kind" in session:
            kind_data = {
                "kind": session['kind']
            }
            return render_template('index.html',
                                company = Company.get_all(), 
                                position_kind = Position.get_kind(kind_data),
                                company_user = Company.get_one(data)
                                )

        if "place" in session:
            place_data = {
                "place": session['place']
            }
            return render_template('index.html',
                                company = Company.get_all(), 
                                position_place = Position.get_place(place_data),
                                company_user = Company.get_one(data)
                                )
        return render_template('index.html',
                                company_user = Company.get_one(data), 
                                positions = Position.get_all(),
                                company = Company.get_all())
    

    return render_template('index.html',
                            company = Company.get_all(), 
                            positions = Position.get_all())
                        
@app.route('/user_login')
def user_login():
    return render_template('user/login.html')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    
    return redirect('/')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/job_kind', methods=['POST'])
def kind_job():
    session['kind'] = request.form['title']
    return redirect('/')

@app.route('/job_place', methods=['POST'])
def place_job():
    session['place'] = request.form['place']
    return redirect('/')