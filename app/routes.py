from flask import Blueprint, jsonify, request

main_bp = Blueprint('main', __name__)

# In-memory storage for demo purposes
members = [
    {"id": 1, "name": "Alice", "plan": "Premium"},
    {"id": 2, "name": "Bob", "plan": "Basic"}
]

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@main_bp.route('/members', methods=['GET'])
def get_members():
    return jsonify(members), 200

@main_bp.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data or not 'name' in data or not 'plan' in data:
        return jsonify({"error": "Bad Request"}), 400
    
    new_id = members[-1]['id'] + 1 if members else 1
    new_member = {
        "id": new_id,
        "name": data['name'],
        "plan": data['plan']
    }
    members.append(new_member)
    return jsonify(new_member), 201
