from flask import request, Blueprint, jsonify
from ..models import User, Product, Postagem
from flask_jwt_extended import jwt_required
from ..extensions import db

#not ready for production yet

postagem_api = Blueprint('postagem_api', __name__)

#todo: proteger essa rota
@postagem_api.route('/postagens/post/', methods=['POST'])
def create_post():

    data = request.json
    #id, caption, img_url, product_id, owner_id

    product_id = data.get('product_id')
    owner_id = data.get('owner_id')
    caption = data.get('caption')
    img_url = 'url/#' #<--- implementar serviço de armazenamento de imagem aqui

    if not data or not caption or not owner_id or not product_id:
        return {'error': 'algum dado faltando no body'}, 400

    postagem = Postagem(caption=caption, img_url=img_url, product_id=product_id, owner_id=owner_id)

    db.session.add(postagem)
    db.session.commit()

    return postagem.json(), 201