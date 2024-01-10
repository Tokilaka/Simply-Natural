from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import backref

from extensions import db, app, login_manager


class BaseModel:
  def create(self):
    db.session.add(self)
    db.session.commit()
    
  def save(self):
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    

class User(db.Model, BaseModel, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True)
  username = db.Column(db.String, unique=True)
  password = db.Column(db.String)
  
  role = db.Column(db.String, default="guest")
  
  def __init__(self, email, username, password, role="guest"):
    self.email = email
    self.username = username
    self.password = generate_password_hash(password)
    self.role = role
    
  def check_password(self, password):
    return check_password_hash(self.password, password)
    

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


class Product(db.Model, BaseModel):
  id = db.Column(db.Integer, primary_key=True)
  category_id = db.Column(db.ForeignKey("product_category.id"))
  name = db.Column(db.String, nullable=False)
  price = db.Column(db.Float, nullable=False)
  discount = db.Column(db.Boolean, default=False) 
  discount_price = db.Column(db.Float)
  img = db.Column(db.String)
  description = db.Column(db.Text)
  
  category = db.relationship("ProductCategory")
  
class ProductCategory(db.Model, BaseModel):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  
  product = db.relationship("Product")
  

class Cart(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    
    user = db.relationship("User", backref=backref("cart", uselist=False))

class CartItem(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    cart = db.relationship("Cart")
    product = db.relationship("Product")
  
  
if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    
    user = User(username="example_user", email="tokiladevdo@gmail.com", password="paroli!1", role="admin")
    cart = Cart(user=user)
    cart.create()