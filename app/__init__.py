from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate
from .user.controllers import user_api
from .product.controllers import product_api
from .postagem.controllers import postagem_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(user_api)
    app.register_blueprint(product_api)
    app.register_blueprint(postagem_api)

    return app
