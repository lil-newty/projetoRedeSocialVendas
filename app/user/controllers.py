from flask import Blueprint, request, render_template, jsonify
from flask_jwt_extended import jwt_required, create_access_token, decode_token
from ..extensions import db
from ..models import User
import bcrypt


user_api = Blueprint('user_api', __name__)


@user_api.route('/users/login/', methods=['POST'])
def login():

    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not data or not email or not password:
        return {'error': 'dados insuficientes'}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
        return {'error': 'dados invalidos'}, 400

    token = create_access_token(identity=user.id)

    return {'token': token}, 200


@user_api.route('/users/', methods=['POST'])
def create():

    data = request.json

    name = data.get('name')
    email = data.get('email')
    idade = data.get('idade')
    password = data.get('password')
    permission = 'usr'

    if not name or not email or not password:
        return {'error': 'Dados insuficientes'}, 400

    user_check = User.query.filter_by(email=email).first()

    if user_check:
        return {'error': 'Usuario já cadastrado'}, 400

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User(name=name, 
                email=email, 
                idade=idade, 
                permission=permission,
                password_hash=password_hash)

    db.session.add(user)
    db.session.commit()

    return user.json(), 200


@user_api.route('/users/', methods=['GET'])
@jwt_required
def index():

    data = request.args

    idade = data.get('idade')

    if not idade:
        users = User.query.all()
    else:

        idade = idade.split('-')

        if len(idade) == 1:

            users = User.query.filter_by(idade=idade[0])
        else:

            users = User.query.filter(
                db.and_(User.idade >= idade[0], User.idade <= idade[1]))

    return jsonify([user.json() for user in users]), 200


@user_api.route('/users/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@jwt_required
def user_detail(id):

    user = User.query.get_or_404(id)

    if request.method == 'GET':
        return user.json(), 200

    if request.method == 'PUT':

        data = request.json

        if not data:
            return {'error': 'Requisição precisa de body'}, 400

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return {'error': 'Dados insuficientes'}, 400

        if User.query.filter_by(email=email).first() and email != user.email:
            return {'error': 'Email já cadastrado'}, 400

        user.name = name
        user.email = email

        db.session.add(user)
        db.session.commit()

        return user.json(), 200

    if request.method == 'PATCH':

        data = request.json

        if not data:
            return {'error': 'Requisição precisa de body'}, 400

        email = data.get('email')

        if User.query.filter_by(email=email).first() and email != user.email:
            return {'error': 'Email já cadastrado'}, 400

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.idade = data.get('idade', user.idade)

        db.session.add(user)
        db.session.commit()

        return user.json(), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return {}, 204

