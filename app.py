from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
from functions import is_gold_investment_query,get_gold_investment_response
import uuid
from models import db, Users, GoldPurchase, ChatHistory
load_dotenv()

app = Flask(__name__)
database_url = os.getenv('DATABASE_URL')
client = OpenAI(api_key=os.getenv("OPENAI"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


CURRENT_GOLD_PRICE_PER_GRAM = 6247.50


@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.json.get("user_id")
    message = request.json.get("message")
    
    if not user_id or not message:
        return jsonify({"error": "user_id and message are required","success":"False"}), 400
    
    is_gold_query = is_gold_investment_query(message)
    
    if not is_gold_query:
        response_text = "I'm your gold investment assistant! I can help you with questions about gold investments, digital gold, gold SIP, and more. Please ask me anything about gold investments!"
        intent = "non_gold_query"
    else:
        response_text = get_gold_investment_response(message)
        intent = "gold_investment_query"
    
    newchat=ChatHistory(user_id=user_id,message=message,response=response_text,intent=intent)
    db.session.add(newchat)
    db.session.commit()
    return jsonify({
        "reply": response_text,
        "user_id": user_id,
        "intent": intent,
        "investment_url":"/buy_gold" if GoldPurchase else None,
        "status": "success"
    })

@app.route("/buy_gold",methods=["POST"])
def buyingGold():
    try:
        user_id = request.json.get("user_id")
        amount_inr = request.json.get("amount_inr")
        user_name = request.json.get("user_name", "Guest User")
        user_email = request.json.get("user_email", "")
        user_phone = request.json.get("user_phone", "")
        # print(goldgr)
        if not user_id or not amount_inr:
            return jsonify({"error": "user_id and amount_inr are required","success":"False"}), 400
        if float(amount_inr) < 10:
                return jsonify({"error": "Minimum investment amount is ₹10","success":"False"}), 400
        gold_grams = float(amount_inr) / CURRENT_GOLD_PRICE_PER_GRAM
        transaction_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"
        existing_user = Users.query.filter_by(user_id=user_id).first()
        if not existing_user:
            new_user = Users(user_id=user_id,name=user_name,email=user_email,phone=user_phone,profile_completed=True)
            db.session.add(new_user)
        else:
            existing_user.name = user_name
            existing_user.email = user_email
            existing_user.phone = user_phone
            existing_user.profile_completed = True
        new_purchase = GoldPurchase(transaction_id=transaction_id,user_id=user_id,amount_inr=float(str(amount_inr)),gold_grams=float(str(round(gold_grams, 4))),gold_price_per_gram=float(str(CURRENT_GOLD_PRICE_PER_GRAM)))
        db.session.add(new_purchase)
        db.session.commit()
        total_holdings = db.session.query(db.func.sum(GoldPurchase.gold_grams).label('total_gold'),db.func.sum(GoldPurchase.amount_inr).label('total_invested')).filter(GoldPurchase.user_id == user_id,GoldPurchase.status == 'completed').first()
        
        return jsonify({
            "message": "Gold purchase successful!",
            "transaction_details": {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "amount_invested": float(amount_inr),
                "gold_purchased_grams": round(gold_grams, 4),
                "gold_price_per_gram": CURRENT_GOLD_PRICE_PER_GRAM,
                "purchase_date": datetime.now().isoformat(),
                "status": "completed"
            },
            "total_gold_grams": round(float(total_holdings.total_gold or 0), 4),
            "total_invested_inr": float(total_holdings.total_invested or 0),
            "current_value_inr": round(float(total_holdings.total_gold or 0) * CURRENT_GOLD_PRICE_PER_GRAM, 4),
            "success":"True"
        })
    except:
        db.session.rollback()
        return jsonify({"message":"Something went wrong","success":"False"}), 500


if __name__ == "__main__":
    app.run(debug=True)
