from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import pprint
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'coding_dojo_wall'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = '''
        INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;'''
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = '''
        SELECT * FROM users
        ;'''
        results = connectToMySQL(db).query_db(query)
        users = []
        for db_row in results:
            users.append(cls(db_row))
        pprint.pprint(results, sort_dicts = False)
        return users
    # return the list of class instances
    # whenever we are sending back data, we want it to be in the form of a class instance
    # a class instance is a way to keep all of your data organized, and attributes can be added on


    @classmethod
    def get_user_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])



    @staticmethod
    def validate_user_registration(user):
        is_valid = True
        # query = 'SELECT * FROM users WHERE email = %(email)s;'
        # result = connectToMySQL(db).query_db(query, user)
        result = User.get_user_by_email(user)
        # this will return either False or a class instance
        if result:
        # if it returns a class instance, that means the email is already taken
            flash('Invalid Email/Password', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email/Password', 'register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First Name must be at least 2 characters.', 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last Name must be at least 2 characters.', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
            is_valid = False
        if len(user['content']) == 0:
            flash('Post cannot be blank.', 'post')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match!', 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_post_and_comments(content):
        pprint.pprint(content, sort_dicts=False)
        is_valid = True
        if len(content['content']) == 0:
            flash('Content must not be blank.', 'post')
            is_valid = False
        return is_valid


    # @classmethod
    # def update_user(cls, data):
    #     query = '''
    #     UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s
    #     ;'''
    #     # data = {'id': id}
    #     return connectToMySQL(db).query_db(query, data)


    # @classmethod
    # def delete_user(cls, data):
    #     query = '''
    #     DELETE FROM users WHERE id = %(id)s
    #     ;'''
    #     data = {'id': id}
    #     return connectToMySQL(db).query_db(query, data)