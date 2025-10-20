from database import db

class Products(db.Model):
    __tablename__ = 'PIS_products_master'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    description = db.Column(db.Text)
    specifications = db.Column(db.JSON)
    features = db.Column(db.JSON)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=0)
    warranty = db.Column(db.String(255))

class ProductReviews(db.Model):
    __tablename__ = 'PIS_product_reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('PIS_products_master.id'), nullable=False)
    reviewer_name = db.Column(db.String(100))
    rating = db.Column(db.Float)
    review_text = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.DateTime, default=db.func.now())