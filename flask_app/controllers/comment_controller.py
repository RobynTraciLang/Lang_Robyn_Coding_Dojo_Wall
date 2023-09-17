from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user_model
from flask_app.models import comment_model, post_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/post_comment/<int:id>', methods = ['POST'])
def post_a_comment(id):
    if 'user_id' not in session:
        flash('You need to log in to access this page.', 'not_logged_in')
        return redirect('/')
    data = {
        'content': request.form['content'],
        'users_id': session['user_id'],
        'posts_id': id
    }
    comment_model.Comment.create_comment(data)
    return redirect('/wall')

@app.route('/delete_comment/<int:id>')
def delete_a_comment(id):
    comment_model.Comment.delete_comment(id)
    return redirect('/wall')

@app.route('/edit_comment/<int:id>')
def display_edit_comment_page(id):
    comment = comment_model.Comment.get_comment_by_id(id)
    return render_template('5_edit_recipe.html', comment = comment)

@app.route('/edit_comment/<int:id>', methods = ['POST'])
def edit_comment(id):
    if not user_model.User.validate_post_and_comments(request.form):
        return redirect(f'/edit_comment/{id}')
    data = {
        'id': id,
        'content': request.form['content']
    }
    comment_model.Comment.edit_comment(data)
    return redirect('/wall')