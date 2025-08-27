from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI"))
import random
CURRENT_GOLD_PRICE_PER_GRAM = 6247.50
def is_gold_investment_query(message):
    gold_keywords = [
        'gold', 'investment', 'digital gold', 'gold price', 'sip', 
        'inflation', 'hedge', 'precious metals', 'gold etf', 'gold fund',
        'buy gold', 'invest', 'portfolio', 'diversify'
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in gold_keywords)


def get_gold_investment_response(message):
    try:
        system_prompt = f"""You are a gold investment assistant for Simplify Money App. 
        Current gold price: ₹{CURRENT_GOLD_PRICE_PER_GRAM} per gram.
        
        Your role:
        1. Provide helpful, accurate information about gold investments
        2. Always end responses with a gentle nudge to consider digital gold investment through Simplify Money App
        3. Be conversational and helpful, not pushy
        4. Focus on benefits like inflation hedge, portfolio diversification, and accessibility of digital gold
        5. Keep responses concise but informative
        
        Available investment facts:
        - Digital gold starting from ₹1
        - Backed by physical gold in secure vaults
        - Instant liquidity - convert to cash anytime
        - No storage hassles
        - Gold SIP available for regular investments
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        if "invest" not in ai_response.lower() or "digital gold" not in ai_response.lower():
            ai_response += f"\n\n💰 Ready to start your gold investment journey? You can buy digital gold starting from just ₹10 through our secure platform. Would you like to make a purchase?"
        
        return ai_response
        
    except Exception as e:
        fallback_responses = [
            f"Gold is an excellent hedge against inflation! At current price of ₹{CURRENT_GOLD_PRICE_PER_GRAM} per gram, digital gold offers easy entry into precious metal investments. Start with just ₹10! Would you like to purchase some digital gold?",
            f"Digital gold is revolutionizing how we invest in gold! No storage worries, instant liquidity, and backed by physical gold. Current rate: ₹{CURRENT_GOLD_PRICE_PER_GRAM}/gram. Interested in making a small purchase to get started?",
            "Gold SIP is a smart way to build wealth systematically! Regular small investments help average out market volatility. Ready to start your gold investment journey with us?"
        ]
        return fallback_responses[random.randint(0,2)]

