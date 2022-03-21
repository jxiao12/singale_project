from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, company, position

class Position:
    db_name = "single"

    def __init__(self, data):
        self.id = data["id"]
        self.positions = data["positions"]
        self.salary = data["salary"]
        self.introduction = data["introduction"]
        self.create_at = data['create_at']
        self.upload_at = data['upload_at']
        self.company_id = data['company_id']
        self.creator = None


    @classmethod
    def save(cls, data):
        query = "INSERT INTO position (positions, salary, introduction, company_id) VALUES(%(positions)s,%(salary)s, %(introduction)s, %(company_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM position;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        posi = []
        for row in results:
            posi.append( cls(row) )
        return posi

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM position WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_one_with_creator(cls, data):
        query = "SELECT * FROM company LEFT JOIN position ON company.id = position.company_id WHERE position.company_id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        one_show = cls(result[0])
        company_info = {
            'id':result[0]['company_id'],
            'name':result[0]['name'],
            'location':result[0]['location'],
            'company_email':result[0]['company_email'],
            'company_password':result[0]['company_password'],
            'create_at':result[0]['create_at'],
            'upload_at':result[0]['upload_at'],
        }
        one_user = company.Company(company_info)
        one_show.creator = one_user
        return one_show

    @classmethod
    def update(cls, data):
        query = "UPDATE position SET positions=%(positions)s, salary=%(salary)s, introduction=%(introduction)s, update_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM position WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(position):
        is_valid = True
        if len(position['positions']) < 1:
            is_valid = False
            flash("Position must be at least 3 characters","position")
        if len(position['salary']) < 0:
            is_valid = False
            flash("Bad position","position")
        return is_valid