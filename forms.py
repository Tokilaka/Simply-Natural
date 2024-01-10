from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField, IntegerField, SubmitField, EmailField, PasswordField, TextAreaField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired

class AddProductForm(FlaskForm):
  name = StringField("Product Name", validators=[DataRequired()])
  price = FloatField("Product Price", validators=[DataRequired()])
  img = FileField("Prodouct Photo", validators=[FileRequired()])
  description = TextAreaField("Product Info", validators=[DataRequired()])
  discount = BooleanField("Discount")
  discount_price = FloatField("Discounted Price")
  category_id = SelectField("Category",coerce=int, validators=[DataRequired()])
  
  submit = SubmitField("Submit")  
  
class AddProductCategoryForm(FlaskForm):
  name = StringField("Category Name", validators=[DataRequired()])
  submit = SubmitField("Submit")
  
  
class AddProductToCart(FlaskForm):
  quantity = IntegerField(validators=[DataRequired()])
  submit = SubmitField("ADD TO CART")  

  
class LogInForm(FlaskForm):
  email = EmailField("Email address", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  
  submit = SubmitField("LOG IN")
  
  
class RegisterForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  email = EmailField("Email address",  validators=[DataRequired()])
  password = PasswordField("Enter password", validators=[DataRequired()])
  confirm = PasswordField("Confirm password", validators=[DataRequired()])
  
  submit = SubmitField("REGISTER") 
  
  