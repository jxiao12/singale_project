from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = "single"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.create_at = data['create_at']
        self.upload_at = data['upload_at']
        self.company = []


    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_company(cls, data):
        query = "SELECT * FROM user LEFT JOIN company ON user.id = company.user_id WHERE company.user_id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        company = []
        for i in result:
            company_info = {
                "id":i["company.id"],
                "name": i["name"],
                "location": i["location"],
                "company_email": i["company_email"],
                "company_password": i["company_password"],
            }
            company.append(company_info)
        return company

        # one_show = cls(result[0])
        # creator_info = {
        #     'id':result[0]['user_id'],
        #     'first_name':result[0]['first_name'],
        #     'last_name':result[0]['last_name'],
        #     'email':result[0]['email'],
        #     'password':result[0]['password'],
        #     'create_at':result[0]['create_at'],
        #     'upload_at':result[0]['upload_at'],
        # }
        # one_user = user.User(creator_info)
        # one_show.creator = one_user
        # return one_show

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid