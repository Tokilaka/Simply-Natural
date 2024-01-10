from flask import redirect,url_for,render_template,request, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddProductForm, LogInForm, RegisterForm, AddProductCategoryForm, AddProductToCart
from models import Product, ProductCategory, User, CartItem, Cart
from extensions import app, db


@app.route('/',methods=['GET','POST'])
def home():
  if request.method=='POST':
    # Handle POST Request here
    return render_template('base.html')
  return render_template('base.html', )


@app.route("/login", methods=["GET", "POST"])
def login():
  form = LogInForm()
  
  if form.validate_on_submit():
    user = User.query.filter(User.email == form.email.data).first()
    if user and user.check_password(form.password.data):
      login_user(user)
      return redirect("/")
    
  return render_template("logIn.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
  logout_user()
  
  return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
  form = RegisterForm()
  
  if form.validate_on_submit():
    existing_user = User.query.filter(User.email == form.email.data).first()
    if form.password.data != form.confirm.data:
      flash("Passwords don't match")
    elif existing_user:
      flash("Email already used")
    else:
      new_user = User(username=form.username.data, password=form.password.data, email=form.email.data)
      cart = Cart(user=new_user)
      cart.create()
      return redirect("/")
    
  messages = list(get_flashed_messages())  
  return render_template("register.html", form=form, messages=messages)  


@app.route("/store", methods=["GET", "POST"])
def store():
  products = Product.query.paginate(per_page=6, page=1)
  
  return render_template("store.html", products=products)

@app.route("/store/page/<int:page_id>", methods=["GET", "POST"])
def page(page_id):
  products = Product.query.paginate(per_page=6, page=page_id)
  
  return render_template("store.html", products=products, page_id=page_id)

@app.context_processor
def inject_products():
    categories = ProductCategory.query.all()
    return dict(categories=categories)

@app.route("/category/<int:category_id>", methods=["GET", "POST"])
def category(category_id):
  category = ProductCategory.query.get(category_id)
  products = category.product
  
  return render_template("search.html", products=products)


@app.route("/store/<string:name>", methods=["GET", "POST"])
def search(name):
  products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
  
  
  return render_template("search.html", products=products)


@app.route("/store/view_product/<int:product_id>",  methods=["GET", "POST"])
def view_product(product_id):
  product = Product.query.get(product_id)
  
  category = None
  if product.category_id:
    category = ProductCategory.query.get(product.category.id).name
  form = AddProductToCart()
  
  if not product:
    # add error page
    pass 
  
  if form.validate_on_submit():
    if not current_user.is_authenticated:
      return redirect('/login')
    
    new_item = CartItem(cart_id=current_user.id,
                        product_id=product_id,
                        quantity=form.quantity.data)
    new_item.create()
    return redirect('/store')
  
  return render_template("viewProduct.html", product=product, category=category, form=form)

@app.route("/cart", methods=["GET", "POST"])
def cart():
  cart_id = current_user.cart.id

  items_in_cart = (
      db.session.query(CartItem, Product)
      .join(Product, CartItem.product_id == Product.id)
      .filter(CartItem.cart_id == cart_id)
      .all()
  )
  total = 0.0

  for item, product in items_in_cart:
    if product.discount:
      item_total_price = product.discount_price * item.quantity
      total += item_total_price
    else:
      item_total_price = product.price * item.quantity
      total += item_total_price
  
  total_price = round(total, 2)
  
  return render_template("cart.html", items_in_cart=items_in_cart, total_price=total_price)

@app.route("/cart/remove_item/<int:cart_item_id>")
def remove_cart_item(cart_item_id):
  cart_item = CartItem.query.get(cart_item_id)
  if cart_item and cart_item.cart.user == current_user:
    cart_item.delete()
  
  return redirect("/cart")

@app.route('/add_product', methods=["GET", "POST"])
@login_required
def add_product():
  if current_user.role != "admin":
    return redirect("/")
  
  form = AddProductForm()
  
  form.category_id.choices = [(category.id, category.name) for category in ProductCategory.query.all()]
 
  if form.validate_on_submit():
    file = form.img.data
    filename = file.filename
    img_path = path.join(app.root_path, "static", "img", "products")
    file.save(path.join(img_path, filename))
    
    new_product=Product(name=form.name.data, 
                        price=form.price.data, 
                        discount=form.discount.data, 
                        discount_price=form.discount_price.data,
                        img=filename,
                        description=form.description.data,
                        category_id=form.category_id.data
                        )
    new_product.create()    
    
    return redirect(url_for("add_product"))
      
  return render_template("addProduct.html",form=form ,category=category)

@app.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
  if current_user.role != "admin":
    return redirect("/")
  
  category = AddProductCategoryForm()  
  
  if category.validate_on_submit():
    new_category = ProductCategory(name=category.name.data)
    new_category.create()   
    
    return redirect(url_for("add_category"))
  
  return render_template("addCategory.html", category=category)

@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
  if current_user.role != "admin":
    return redirect("/")
  
  product = Product.query.get(product_id)
  if not product:
    # handle error
    pass
  
  product.delete()

  return redirect("/add_product")

@app.route("/delete_category/<int:category_id>")
@login_required
def delete_category(category_id):
  if current_user.role != "admin":
    return redirect("/")
  
  product_category = ProductCategory.query.get(category_id)
  if not product_category:
    # handle error
    pass
  
  product_category.delete()
  
  return redirect("/store")

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
  if current_user.role != "admin":
    return redirect("/")
  
  product = Product.query.get(product_id)
  
  if not product:
    # error handle
    pass
  
  form = AddProductForm(name=product.name, 
                        price=product.price, 
                        img=product.img, 
                        description=product.description, 
                        discount=product.discount, 
                        discount_price=product.discount_price,
                        category_id=product.category_id
                        )
  
  form.category_id.choices = [(category.id, category.name) for category in ProductCategory.query.all()]
  
  if form.validate_on_submit():
    file = form.img.data
    filename = file.filename
    img_path = path.join(app.root_path, "static", "img", "products")
    file.save(path.join(img_path, filename))
    
    product.name=form.name.data
    product.price=form.price.data 
    product.discount=form.discount.data
    product.discount_price=form.discount_price.data
    product.img=filename
    product.description=form.description.data
    product.category_id=form.category_id.data
    
    product.save()
  
  return render_template("addProduct.html", form=form)

@app.route("/admin_panel")
def admin_panel():
  if current_user.role != "admin":
    return redirect("/")
  
  return render_template("adminPanel.html")