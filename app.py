from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from config import Config
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import MongoOperations


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config.from_object(Config)

mongo = PyMongo()
jwt = JWTManager()

# Initialize extensions
mongo.init_app(app)
jwt.init_app(app)

mongodb = MongoOperations(mongo)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Here you should validate the username and password with your user model
    # For simplicity, let's assume it's valid and return a JWT
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/sales', methods=['POST'])
@jwt_required()
def create_sale():
    current_user = get_jwt_identity()
    data = request.get_json()
    sales_record = mongodb.create_sales_record(current_user, data)
    return jsonify(sales_record), 201

@app.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    current_user = get_jwt_identity()
    sales_records = mongodb.get_sales_records(current_user)
    return jsonify(sales_records), 200

@app.route('/sales/<sale_id>', methods=['GET'])
@jwt_required()
def get_sale(sale_id):
    current_user = get_jwt_identity()
    sale = mongodb.get_sales_record_by_id(current_user, sale_id)
    if sale:
        return jsonify(sale), 200
    return jsonify({"msg": "Sale not found"}), 404

@app.route('/sales/<sale_id>', methods=['PUT'])
@jwt_required()
def update_sale(sale_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    mongodb.update_sales_record(sale_id, current_user, data)
    return jsonify({"msg": "Sale updated"}), 200

@app.route('/sales/<sale_id>', methods=['DELETE'])
@jwt_required()
def delete_sale(sale_id):
    current_user = get_jwt_identity()
    mongodb.delete_sales_record(sale_id, current_user)
    return jsonify({"msg": "Sale deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
