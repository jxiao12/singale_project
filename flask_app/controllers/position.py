from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.company import Company
from flask_app.models.position import Position
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/position')
def new_position():
    if 'company_id' not in session:
        return redirect('/')
    data = {
        "id":session["company_id"]
    }
    return render_template('new_position.html',company=Company.get_one(data))

@app.route('/create/position',methods=['POST'])
def create_position():
    if 'user_id' not in session:
        return redirect('/')
    if not Position.validate_recipe(request.form):
        return redirect('/new/position')
    data = {
        "positions": request.form["positions"],
        "salary": request.form["salary"],
        "introduction": request.form["introduction"],
        "comapny_id": session["company_id"]
    }
    position = Position.save(data)
    session['id'] = position
    return redirect('/')


@app.route('/destroy_position/<int:id>')
def destroy_position(id):
    if 'company_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    Position.destroy(data)
    return redirect('/')


@app.route('/show_position/<int:id>')
def show_position(id):
    if 'company_id' not in session:
        return render_template("show_pos.html",position=Position.get_one({"id":id}))
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    company_data = {
        "id": session['company_id']
    }
    return render_template("show_pos.html",position=Position.get_one_with_creator(company_data),user=User.get_by_id(user_data))


@app.route('/edit_position/<int:id>')
def edit_position(id):
    if 'company_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_pos.html",position=Position.get_one(data), user=User.get_by_id(user_data))

@app.route('/update/position',methods=['POST'])
def update_position():
    if 'company_id' not in session:
        return redirect('/')
    if not Position.validate_recipe(request.form):
        return redirect('/new/position')

    print(session)

    data = {
        "positions": request.form["positions"],
        "salary": request.form["salary"],
        "introduction": request.form["introduction"],
        "user_id": session["user_id"],
        "id": session["id"]
    }
    Position.update(data)
    return redirect('/')