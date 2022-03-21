from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.company import Company
from flask_app.models.position import Position
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/company')
def new_company():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session['user_id']
    }

    return render_template('new_company.html',user=User.get_by_id(data))

@app.route('/create/company',methods=['POST'])
def create_company():
    if 'user_id' not in session:
        return redirect('/')
    if not Company.validate_recipe(request.form):
        return redirect('/new/company')
    data = {
        "name": request.form["name"],
        "location": request.form["location"],
        "company_email": request.form["company_email"],
        "company_password": request.form["company_password"],
        "user_id": session["user_id"]
    }
    company = Company.save(data)
    session['id'] = company
    return redirect('/')

@app.route('/edit_company/<int:id>')
def edit_company(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_company.html",edit=Company.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/company',methods=['POST'])
def update_company():
    if 'user_id' not in session:
        return redirect('/')
    if not Company.validate_recipe(request.form):
        return redirect('/new/company')

    data = {
        "location": request.form["location"],
        "name": request.form["name"],
        "company_email": request.form["company_email"],
        "company_password": request.form["company_password"],
        "user_id": session["user_id"],
        "id": session["id"]
    }
    Company.update(data)
    return redirect('/')

@app.route('/show_company/<int:id>')
def show_company(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    session['company_id'] = id
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_company.html",
                            company=Company.get_one(data),
                            user=User.get_by_id(user_data),
                            position=Company.get_all_position(data))

@app.route('/destroy_company/<int:id>')
def destroy_tv(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    Company.destroy(data)
    return redirect('/')
