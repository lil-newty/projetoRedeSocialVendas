from .extensions import db


likes = db.Table('likes',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('postagem_id', db.Integer, db.ForeignKey('postagens.id'))
                )

class Postagem(db.Model):
    
    __tablename__ = 'postagens'
    #id, caption, img_url, product_id, owner_id
    id = db.Column(db.Integer, primary_key=True)

    caption = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)

    #cada postagem necessariamente precisa de um produto e de um usuário
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def json(self):

        return {'id': self.id,
                'caption': self.caption,
                'img_url': self.img_url,
                'product_id': self.product_id,
                'owner_id': self.owner_id}


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    idade = db.Column(db.Integer, default=0)

    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=False)

    permission = db.Column(db.String(3), nullable=False) #permission = adm/usr/mod

    products = db.relationship('Product', backref='owner')
    postagens = db.relationship('Postagem', backref='owner')

    def json(self):
        user_json = {'id': self.id,
                     'name': self.name,
                     'email': self.email,
                     'idade': self.idade}
        return user_json


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    postagens = db.relationship('Postagem', backref='produto')

    def json(self):

        return {'name': self.name,
                'desciption': self.description,
                'id': self.id,
                'price':self.price,
                'owner': self.owner.json()}
