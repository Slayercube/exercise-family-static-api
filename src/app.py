import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure, FamilyMember

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
user = FamilyMember("deep", 30, [1, 5])

sidhu_family = FamilyStructure('sidhu')
sidhu_family.add_member(user)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = sidhu_family.get_all_members()
        response_body = [member.__dict__ for member in members]
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = sidhu_family.get_member(member_id)
        if member:
            return jsonify(member.__dict__), 200
        else:
            return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("first_name", "age", "lucky_numbers")):
            return jsonify({"error": "Invalid input"}), 400
        new_member = FamilyMember(data["first_name"], data["age"], data["lucky_numbers"])
        sidhu_family.add_member(new_member)
        return jsonify(new_member.__dict__), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = sidhu_family.delete_member(member_id)
        if result:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)