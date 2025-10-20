from datetime import datetime
from database import db
from models import ProductReviews
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "SQLALCHEMY_DB_URI"
db.init_app(app)
reviews_data = [
    # Coffee Maker
    {"product_id": 9, "reviewer_name": "Alice", "rating": 5.0, "review_text": "Brews coffee perfectly, love the timer!", "review_date": datetime.now()},
    {"product_id": 9, "reviewer_name": "Bob", "rating": 4.0, "review_text": "Good coffee maker, but takes a bit long to heat.", "review_date": datetime.now()},
    {"product_id": 9, "reviewer_name": "Charlie", "rating": 3.0, "review_text": "Average, plastic feels cheap.", "review_date": datetime.now()},
    {"product_id": 9, "reviewer_name": "Dana", "rating": 5.0, "review_text": "Excellent product, easy to clean!", "review_date": datetime.now()},
    {"product_id": 9, "reviewer_name": "Eve", "rating": 2.0, "review_text": "Stopped working after 2 months.", "review_date": datetime.now()},

    # Notebook
    {"product_id": 11, "reviewer_name": "Frank", "rating": 5.0, "review_text": "Love the hardcover and quality pages.", "review_date": datetime.now()},
    {"product_id": 11, "reviewer_name": "Grace", "rating": 4.0, "review_text": "Great notebook but a bit pricey.", "review_date": datetime.now()},
    {"product_id": 11, "reviewer_name": "Hannah", "rating": 3.0, "review_text": "Paper quality is okay, not outstanding.", "review_date": datetime.now()},
    {"product_id": 11, "reviewer_name": "Ian", "rating": 5.0, "review_text": "Perfect for journaling!", "review_date": datetime.now()},
    {"product_id": 11, "reviewer_name": "Jack", "rating": 2.0, "review_text": "Cover scratched easily.", "review_date": datetime.now()},

    # Smartwatch
    {"product_id": 14, "reviewer_name": "Karen", "rating": 5.0, "review_text": "Tracks workouts accurately.", "review_date": datetime.now()},
    {"product_id": 14, "reviewer_name": "Leo", "rating": 4.0, "review_text": "Good battery life, but screen is small.", "review_date": datetime.now()},
    {"product_id": 14, "reviewer_name": "Mia", "rating": 3.0, "review_text": "Average performance, sometimes lags.", "review_date": datetime.now()},
    {"product_id": 14, "reviewer_name": "Nina", "rating": 5.0, "review_text": "Excellent for fitness tracking!", "review_date": datetime.now()},
    {"product_id": 14, "reviewer_name": "Oscar", "rating": 2.0, "review_text": "Bluetooth disconnects frequently.", "review_date": datetime.now()},

    # Bluetooth Speaker
    {"product_id": 17, "reviewer_name": "Paul", "rating": 5.0, "review_text": "Great sound and waterproof!", "review_date": datetime.now()},
    {"product_id": 17, "reviewer_name": "Quinn", "rating": 4.0, "review_text": "Battery lasts long, but bass is low.", "review_date": datetime.now()},
    {"product_id": 17, "reviewer_name": "Rachel", "rating": 3.0, "review_text": "Average sound quality.", "review_date": datetime.now()},
    {"product_id": 17, "reviewer_name": "Sam", "rating": 5.0, "review_text": "Perfect for outdoor use!", "review_date": datetime.now()},
    {"product_id": 17, "reviewer_name": "Tina", "rating": 2.0, "review_text": "Stopped working after a month.", "review_date": datetime.now()},

    # Hair Dryer
    {"product_id": 20, "reviewer_name": "Uma", "rating": 5.0, "review_text": "Dries hair quickly, love it!", "review_date": datetime.now()},
    {"product_id": 20, "reviewer_name": "Vik", "rating": 4.0, "review_text": "Good for travel, lightweight.", "review_date": datetime.now()},
    {"product_id": 20, "reviewer_name": "Will", "rating": 3.0, "review_text": "Noise is a bit high.", "review_date": datetime.now()},
    {"product_id": 20, "reviewer_name": "Xena", "rating": 5.0, "review_text": "Excellent, compact and powerful.", "review_date": datetime.now()},
    {"product_id": 20, "reviewer_name": "Yara", "rating": 2.0, "review_text": "Stopped working after a few uses.", "review_date": datetime.now()},

    # External Hard Drive
    {"product_id": 22, "reviewer_name": "Zack", "rating": 5.0, "review_text": "Fast transfer speed, very reliable.", "review_date": datetime.now()},
    {"product_id": 22, "reviewer_name": "Amy", "rating": 4.0, "review_text": "Compact and portable.", "review_date": datetime.now()},
    {"product_id": 22, "reviewer_name": "Brian", "rating": 3.0, "review_text": "Sometimes disconnects unexpectedly.", "review_date": datetime.now()},
    {"product_id": 22, "reviewer_name": "Clara", "rating": 5.0, "review_text": "Exactly what I needed, perfect!", "review_date": datetime.now()},
    {"product_id": 22, "reviewer_name": "David", "rating": 2.0, "review_text": "Stopped working after 6 months.", "review_date": datetime.now()},
]

with app.app_context():  # <-- this is crucial
    db.session.bulk_insert_mappings(ProductReviews, reviews_data)
    db.session.commit()
    print("All reviews inserted successfully!")