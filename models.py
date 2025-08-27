from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    profile_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id= db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    intent= db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

class GoldPurchase(db.Model):
    __tablename__ = 'gold_purchases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.String(255), nullable=False)
    amount_inr = db.Column(db.Numeric(12, 2), nullable=False)
    gold_grams = db.Column(db.Numeric(10, 4), nullable=False)
    gold_price_per_gram = db.Column(db.Numeric(10, 2), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), default='completed')
