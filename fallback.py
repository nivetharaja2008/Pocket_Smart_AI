def home_fallback(req):
    return {
        "planner": "home",
        "source": "fallback",
        "summary": "Basic home budget plan generated without Gemini.",
        "budget_allocation": {
            "Furniture": round(req.budget * 0.30, 2),
            "Decor": round(req.budget * 0.20, 2),
            "Lighting": round(req.budget * 0.15, 2),
            "Storage": round(req.budget * 0.20, 2),
            "Miscellaneous": round(req.budget * 0.15, 2),
        },
        "recommendations": [
            {
                "name": "Modern Storage Unit",
                "category": "Storage",
                "price": 2500,
                "rating": 4.2,
                "discount": 10,
                "platform": "General",
                "emoji": "🗄️",
                "unit": "item",
                "reason": "Useful for organized storage."
            },
            {
                "name": "LED Decorative Light",
                "category": "Lighting",
                "price": 1200,
                "rating": 4.3,
                "discount": 5,
                "platform": "General",
                "emoji": "💡",
                "unit": "set",
                "reason": "Adds warm lighting to the room."
            }
        ],
        "tips": [
            "Compare prices before purchasing.",
            "Keep a small amount aside for unexpected expenses."
        ]
    }


def party_fallback(req):
    return {
        "planner": "party",
        "source": "fallback",
        "summary": "Basic party budget plan generated without Gemini.",
        "budget_allocation": {
            "Food": round(req.budget * 0.35, 2),
            "Decoration": round(req.budget * 0.20, 2),
            "Entertainment": round(req.budget * 0.15, 2),
            "Gifts": round(req.budget * 0.15, 2),
            "Miscellaneous": round(req.budget * 0.15, 2),
        },
        "recommendations": [
            {
                "name": "Balloon Decoration Set",
                "category": "Decoration",
                "price": 799,
                "rating": 4.3,
                "discount": 10,
                "platform": "General",
                "emoji": "🎈",
                "unit": "set",
                "reason": "Simple decoration option for a party."
            },
            {
                "name": "Party Cups and Plates",
                "category": "Party Supplies",
                "price": 499,
                "rating": 4.2,
                "discount": 5,
                "platform": "General",
                "emoji": "🥤",
                "unit": "set",
                "reason": "Useful for serving guests."
            },
            {
                "name": "Birthday Banner",
                "category": "Decoration",
                "price": 299,
                "rating": 4.1,
                "discount": 0,
                "platform": "General",
                "emoji": "🎉",
                "unit": "item",
                "reason": "Adds a festive touch to the venue."
            }
        ],
        "tips": [
            "Compare food and decoration prices.",
            "Keep some budget for unexpected expenses."
        ]
    }


def jewelry_fallback(req):
    return {
        "planner": "jewelry",
        "source": "fallback",
        "summary": "Basic jewelry recommendation generated without Gemini.",
        "budget_allocation": {
            "Necklace": round(req.budget * 0.40, 2),
            "Earrings": round(req.budget * 0.25, 2),
            "Bangles": round(req.budget * 0.20, 2),
            "Miscellaneous": round(req.budget * 0.15, 2),
        },
        "recommendations": [
            {
                "name": "Elegant Necklace Set",
                "category": "Necklace",
                "price": 1800,
                "rating": 4.3,
                "discount": 10,
                "platform": "General",
                "emoji": "📿",
                "unit": "set",
                "reason": "Suitable for an elegant occasion."
            },
            {
                "name": "Classic Earrings",
                "category": "Earrings",
                "price": 799,
                "rating": 4.2,
                "discount": 5,
                "platform": "General",
                "emoji": "✨",
                "unit": "pair",
                "reason": "Easy to pair with different outfits."
            }
        ],
        "tips": [
            "Check the material and size before purchasing.",
            "Compare prices across platforms."
        ]
    }