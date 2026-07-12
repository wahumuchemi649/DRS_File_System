from Department.views import departments, dept_documents, dept_members
from flask import Blueprint


Department_bp = Blueprint('Department', __name__)

@Department_bp.route('/departments', methods=['GET'])
def get_departments():
    return departments()
@Department_bp.route('/department_members/<int:UserId>',methods=['GET'])
def department_members_route(UserId):
    return dept_members(UserId)
@Department_bp.route('/department_documents/<int:UserId>',methods=['GET'])
def department_documents_route(UserId):
    return dept_documents(UserId)