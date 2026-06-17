from Admin.models import Admin
from flask import Blueprint
from Admin.views import manage_users, update_user, delete_user, create_user, manage_departments, get_documents,delete_document
from Admin.views import get_stats,add_document,search_documents,change_document_status,view_document
Admin_bp = Blueprint('Admin', __name__)

@Admin_bp.route('/manage_users', methods=['GET'])
def manage_users_route():
    return manage_users()

@Admin_bp.route('/update_user', methods=['PUT'])
def update_user_route():
    return update_user()
@Admin_bp.route('/delete_user', methods=['DELETE'])   
def delete_user_route():
    return delete_user()
@Admin_bp.route('/create_user', methods=['POST'])
def create_user_route():
    return create_user()
@Admin_bp.route('/manage_departments', methods=['GET'])
def manage_departments_route():
    return manage_departments()
@Admin_bp.route('/manage_files', methods=['GET'])
def manage_files_route():
    return get_documents()


@Admin_bp.route('/get_stats', methods=['GET'])
def get_statistics():
    return get_stats()
@Admin_bp.route('/add_document', methods=['POST'])
def add_documents():
    return add_document()
@Admin_bp.route('/search_documents', methods=['POST'])
def search_documents_route():
    return search_documents()
@Admin_bp.route('/change_status', methods=['PUT'])
def change_status_route():
    return change_document_status()
@Admin_bp.route('/view_document', methods=['POST'])
def view_document_route():
    return view_document()
@Admin_bp.route('/delete_document',methods=['DELETE'])
def view_delete_document():
    return delete_document()