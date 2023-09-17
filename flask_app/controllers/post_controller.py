from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user_model
from flask_app.models import post_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# display route is foundin user_controller, '/wall'

@app.route('/wall', methods = ['POST'])
def make_a_post():
    if 'user_id' not in session:
        flash('You need to log in to access this page.', 'not_logged_in')
        return redirect('/')
    if not user_model.User.validate_post_and_comments(request.form):
        flash('Post content cannot be blank.')
        return redirect('/wall')
    data = {
        'content': request.form['content'],
        'users_id': session['user_id'],
    }
    post_model.Post.create_post(data)
    return redirect('/wall')

@app.route('/delete_post/<int:id>')
def delete_a_post(id):
    post_model.Post.delete_post(id)
    return redirect('/wall')

@app.route('/edit_post/<int:id>')
def display_edit_post_page(id):
    post = post_model.Post.get_post_by_id(id)
    return render_template('5_edit_recipe.html', post = post)

@app.route('/edit_post/<int:id>', methods = ['POST'])
def edit_post(id):
    if not user_model.User.validate_post_and_comments(request.form):
        return redirect(f'/edit_post/{id}')
    data = {
        'id': id,
        'content': request.form['content']
    }
    post_model.Post.edit_post(data)
    return redirect('/wall')
