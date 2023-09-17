from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model, comment_model
from flask import flash
import pprint
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'coding_dojo_wall'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comments = []

    @classmethod
    def create_post(cls, data):
        query = '''
        INSERT INTO posts (content, users_id) VALUES (%(content)s, %(users_id)s)
        ;'''
        # the prepared statements reference the data I'm passing in in the controller
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_all_posts_with_user(cls):
        query = '''
        SELECT * FROM posts LEFT JOIN users ON posts.users_id = users.id LEFT JOIN comments ON comments.users_id = users.id
        ;'''
        results = connectToMySQL(db).query_db(query)
        posts = []
        for each_post in results:
            post_instance = cls(each_post)
            user_data = {
                'id': each_post['users.id'],
                'first_name': each_post['first_name'],
                'last_name': each_post['last_name'],
                'email': each_post['email'],
                'password': None,
                'created_at': each_post['users.created_at'],
                'updated_at': each_post['users.updated_at'],
            }
            comment_data = {
                'id': each_post['comments.id'],
                'content': each_post['comments.content'],
                'users_id': each_post['comments.users_id'],
                'posts_id': each_post['posts_id'],
                'created_at': each_post['comments.created_at'],
                'updated_at': each_post['comments.updated_at'],
            }
            post_instance.user = user_model.User(user_data)
            post_instance.comments.append(comment_model.Comment(comment_data))
            posts.append(post_instance)
        # pprint.pprint(results, sort_dicts = False)
        # pprint.pprint(posts, sort_dicts=False)
        return posts


    @classmethod
    def get_all_posts_with_comments(cls):
        query = '''
        SELECT * FROM posts
        LEFT JOIN users ON posts.users_id = users.id
        LEFT JOIN comments ON comments.posts_id = posts.id
        LEFT JOIN users AS commenter ON comments.users_id = commenter.id
        ;'''
        results = connectToMySQL(db).query_db(query)
        posts = []
        for each_post in results:
            if len(posts) == 0 or each_post['id'] != posts[len(posts) - 1].id:
                post_instance = cls(each_post)
                user_data = {
                    'id': each_post['users.id'],
                    'first_name': each_post['first_name'],
                    'last_name': each_post['last_name'],
                    'email': each_post['email'],
                    'password': None,
                    'created_at': each_post['users.created_at'],
                    'updated_at': each_post['users.updated_at'],
                }
                post_instance.user = user_model.User(user_data)
                posts.append(post_instance)
            post_instance = posts[len(posts) - 1]
            comment_data = {
                'id': each_post['comments.id'],
                'content': each_post['comments.content'],
                'users_id': each_post['comments.users_id'],
                'posts_id': each_post['posts_id'],
                'created_at': each_post['comments.created_at'],
                'updated_at': each_post['comments.updated_at'],
            }
            comment_instance = comment_model.Comment(comment_data)
            commenter_data = {
                'id': each_post['commenter.id'],
                'first_name': each_post['commenter.first_name'],
                'last_name': each_post['commenter.last_name'],
                'email': each_post['commenter.email'],
                'password': None,
                'created_at': each_post['commenter.created_at'],
                'updated_at': each_post['commenter.updated_at'],
            }
            comment_instance.user = user_model.User(commenter_data)
            post_instance.comments.append(comment_instance)
        # pprint.pprint(results, sort_dicts = False)
        # pprint.pprint(posts, sort_dicts=False)
        return posts

    @classmethod
    def get_post_by_id(cls, data):
        query = '''
        SELECT * from posts
        LEFT JOIN comments ON comments.posts_id = posts.id
        LEFT JOIN users on comments.users_id = comments.id
        WHERE posts.id = %(id)s
        ;'''
        post_id = {
            'id': data
        }
        result = connectToMySQL(db).query_db(query, post_id)
        pprint.pprint(result, sort_dicts=False)
        post_instance = cls(result[0])
        for post in result:
            user_data = {
                'id': post['users.id'],
                'first_name': post['first_name'],
                'last_name': post['last_name'],
                'email': post['email'],
                'password': None,
                'created_at': post['users.created_at'],
                'updated_at': post['users.updated_at'],
            }
            comment_data = {
                'id': post['comments.id'],
                'content': post['comments.content'],
                'created_at': post['comments.created_at'],
                'updated_at': post['comments.updated_at'],
            }
            user_instance = user_model.User(user_data)
            comment_instance = comment_model.Comment(comment_data)
            post_instance.user = user_instance
            post_instance.comments.append(comment_instance)
        return post_instance


    @classmethod
    def edit_post(cls, data):
        query = '''
        UPDATE posts SET content = %(content)s WHERE id = %(id)s
        ;'''
        return connectToMySQL(db).query_db(query, data)
    # takes data dictionary from request.form


    @classmethod
    def delete_post(cls, post_id):
        query = '''
        DELETE FROM posts WHERE id = %(id)s
        ;'''
        data = {'id': post_id}
        return connectToMySQL(db).query_db(query, data)