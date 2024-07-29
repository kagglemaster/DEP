from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'


db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

class Register(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'username': user.username})
            return jsonify(access_token=access_token)
        return jsonify({"message": "Invalid credentials"}), 401

class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = Item.query.all()    
        return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items])

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_item = Item(name=data['name'], description=data.get('description'))
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item created successfully"})

class ItemDetail(Resource):
    @jwt_required()
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return jsonify({"id": item.id, "name": item.name, "description": item.description})

    @jwt_required()
    def put(self, item_id):
        data = request.get_json()
        item = Item.query.get_or_404(item_id)
        item.name = data['name']
        item.description = data.get('description')
        db.session.commit()
        return jsonify({"message": "Item updated successfully"})

    @jwt_required()
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"})


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(ItemList, '/items')
api.add_resource(ItemDetail, '/items/<int:item_id>')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
