from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model, post_model
from flask import flash
import pprint
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



db = 'coding_dojo_wall'

#the many
class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.users_id = data['users_id']
        self.posts_id = data['posts_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.post = None

    @classmethod
    def create_comment(cls, data):
        query = '''
        INSERT INTO comments (content, users_id, posts_id) VALUES (%(content)s, %(users_id)s, %(posts_id)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)
    # this works

    # takes data dictionary from request.form
    # validates data
    # return id? or False if the validations fail

    @classmethod
    def get_all_comments_with_user(cls):
        query = '''
        SELECT * FROM comments LEFT JOIN users ON comments.users_id = users.id
        ;'''
        results = connectToMySQL(db).query_db(query)
        comments = []
        for db_row in results:
            comment_instance = cls(db_row)
            user_data = {
                'id': db_row['users.id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                'email': db_row['email'],
                'password': None,
                'created_at': db_row['users.created_at'],
                'updated_at': db_row['users.updated_at'],
            }
            comment_instance.user = user_model.User(user_data)
            comments.append(comment_instance)
        # pprint.pprint(results, sort_dicts = False)
        return comments
    # this works

    # get all recipes, and the user info for the creators
    # make a list to hold recipe objects to return
    # return the list of class instances
    # whenever we are sending back data, we want it to be in the form of a class instance
    # a class instance is a way to keep all of your data organized, and attributes can be added on

    @classmethod
    def get_all_comments_with_post(cls):
        query = '''
        SELECT * FROM comments LEFT JOIN posts ON comments.users_id = posts.id
        ;'''
        results = connectToMySQL(db).query_db(query)
        comments = []
        for db_row in results:
            comment_instance = cls(db_row)
            post_data = {
                'id': db_row['posts.id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                'email': db_row['email'],
                'password': None,
                'created_at': db_row['posts.created_at'],
                'updated_at': db_row['posts.updated_at'],
            }
            comment_instance.user = post_model.Post(post_data)
            comments.append(comment_instance)
        # pprint.pprint(results, sort_dicts = False)
        return comments
    # this works

    @classmethod
    def get_comment_by_id(cls, data):
        query = '''
        SELECT * from comments
        LEFT JOIN posts ON posts.comments_id = comments.id
        LEFT JOIN users ON posts.users_id = users.id
        WHERE comments.id = %(id)s
        ;'''
        comment_id = {
            'id': data
        }
        result = connectToMySQL(db).query_db(query, comment_id)
        pprint.pprint(result, sort_dicts=False)
        comment_instance = cls(result[0])
        for comment in result:
            user_data = {
                'id': comment['users.id'],
                'first_name': comment['first_name'],
                'last_name': comment['last_name'],
                'email': comment['email'],
                'password': None,
                'created_at': comment['users.created_at'],
                'updated_at': comment['users.updated_at'],
            }
            post_data = {
                'id': comment['posts.id'],
                'content': comment['posts.content'],
                'created_at': comment['posts.created_at'],
                'updated_at': comment['posts.updated_at'],
            }
            user_instance = user_model.User(user_data)
            post_instance = post_model.Post(post_data)
            comment_instance.user = user_instance
            comment_instance.post = post_instance
        return comment_instance
    # get recipe data with user data who created it
    # make a recipe object from the data
    # associate user with recipe
    # return recipe


    @classmethod
    def edit_comment(cls, data):
        query = '''
        UPDATE comments SET content = %(content)s WHERE id = %(id)s
        ;'''
        return connectToMySQL(db).query_db(query, data)
    # takes data dictionary from request.form


    @classmethod
    def delete_comment(cls, comment_id):
        query = '''
        DELETE FROM comments WHERE id = %(id)s
        ;'''
        data = {'id': comment_id}
        return connectToMySQL(db).query_db(query, data)
    # delete recipe using the id