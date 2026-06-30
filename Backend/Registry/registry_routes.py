from flask import Blueprint, request, jsonify
from Registry.register_document import register_document
from Registry.route_document import route_document
from Registry.documents import get_documents_by_status
from Registry.models import Document

registry_bp = Blueprint('registry', __name__)


@registry_bp.route('/documents', methods=['GET'])
def get_documents():
    status = request.args.get('status', 'Received')
    result = get_documents_by_status(status)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200


@registry_bp.route('/documents/register', methods=['POST'])
def register_doc():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    new_doc = Document(
        docType=data.get('docType'),
        IsExternal=data.get('isExternal', False),
        title=data.get('title'),
        filepath=data.get('filepath'),
        deptId=data.get('deptId')
    )
    result = register_document(new_doc)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201


@registry_bp.route('/documents/route', methods=['PUT'])
def route_doc():
    data = request.get_json()
    if not data.get('docId') or not data.get('deptId'):
        return jsonify({"error": "docId and deptId are required"}), 400
    result = route_document(data['docId'], data['deptId'])
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200