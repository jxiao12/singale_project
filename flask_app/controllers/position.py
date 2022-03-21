from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.company import Company
from flask_app.models.position import Position
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/position')
def new_position():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session["user_id"]
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
        "comapny_id": session["id"]
    }
    print(data)
    position = Position.save(data)
    session['id'] = position
    return redirect('/')


@app.route('/destroy_position/<int:id>')
def destroy_position(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    Position.destroy(data)
    return redirect('/')
