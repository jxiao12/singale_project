from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import re
from flask import flash
company_email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Company:
    db_name = "single"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.company_email = data['company_email']
        self.company_password = data['company_password']
        self.create_at = data['create_at']
        self.upload_at = data['upload_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO company (name, location, company_email, company_password, user_id) VALUES(%(name)s, %(location)s, %(company_email)s, %(company_password)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM company;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append( cls(row) )
        return all_recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM company WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_one_with_creator(cls, data):
        query = "SELECT * FROM user LEFT JOIN company ON user.id = company.user_id WHERE company.user_id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        one_show = cls(result[0])
        creator_info = {
            'id':result[0]['user_id'],
            'first_name':result[0]['first_name'],
            'last_name':result[0]['last_name'],
            'email':result[0]['email'],
            'password':result[0]['password'],
            'create_at':result[0]['create_at'],
            'upload_at':result[0]['upload_at'],
        }
        one_user = user.User(creator_info)
        one_show.creator = one_user
        return one_show

    @classmethod
    def update(cls, data):
        query = "UPDATE company SET name=%(name)s, location=%(location)s, company_email=%(company_email)s, company_password=%(company_password)s, upload_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM company WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(company):
        is_valid = True
        if not company_email_REGEX.match(company['company_email']):
            flash("Invalid company_email!!!","register")
            is_valid=False
        if len(company['location']) < 1:
            is_valid = False
            flash("Location must be at least 3 characters","company")
        if len(company['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","company")
        if company['company_email'] == "":
            is_valid = False
            flash("Please enter a date","company")
        if len(company['company_password']) < 5:
            flash("company_password must be at least 5 characters","register")
            is_valid= False
        if company['company_password'] != company['confirm']:
            flash("company_passwords don't match","register")
        return is_valid