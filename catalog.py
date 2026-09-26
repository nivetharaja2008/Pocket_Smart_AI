from urllib.parse import quote_plus


CATALOG = [

    {
        "name": "Warm LED String Lights",
        "category": "lighting",
        "price": 699,
        "rating": 4.5,
        "discount": 30,
        "platform": "Amazon",
        "emoji": "💡"
    },

    {
        "name": "Minimal Wall Art Set",
        "category": "decor",
        "price": 1299,
        "rating": 4.4,
        "discount": 20,
        "platform": "IKEA",
        "emoji": "🖼️"
    },

    {
        "name": "Compact Study Table",
        "category": "furniture",
        "price": 3499,
        "rating": 4.3,
        "discount": 15,
        "platform": "Amazon",
        "emoji": "🪑"
    },

    {
        "name": "Dining Table 4 Seater",
        "category": "furniture",
        "price": 8999,
        "rating": 4.6,
        "discount": 18,
        "platform": "IKEA",
        "emoji": "🍽️"
    },

    {
        "name": "Modern Ceiling Light",
        "category": "lighting",
        "price": 1899,
        "rating": 4.2,
        "discount": 22,
        "platform": "Amazon",
        "emoji": "✨"
    },

    {
        "name": "Decorative Cushion Set",
        "category": "decor",
        "price": 899,
        "rating": 4.5,
        "discount": 25,
        "platform": "Flipkart",
        "emoji": "🛋️"
    },

    {
        "name": "Birthday Balloon Kit",
        "category": "decoration",
        "price": 599,
        "rating": 4.6,
        "discount": 35,
        "platform": "Amazon",
        "emoji": "🎈"
    },

    {
        "name": "Birthday Banner & Props",
        "category": "party supplies",
        "price": 449,
        "rating": 4.4,
        "discount": 28,
        "platform": "Flipkart",
        "emoji": "🎉"
    },

    {
        "name": "Table Decoration Pack",
        "category": "decoration",
        "price": 799,
        "rating": 4.3,
        "discount": 20,
        "platform": "Amazon",
        "emoji": "🌸"
    },

    {
        "name": "Party Cups & Plates",
        "category": "party supplies",
        "price": 699,
        "rating": 4.5,
        "discount": 15,
        "platform": "Flipkart",
        "emoji": "🥤"
    },

    {
        "name": "Family Party Game Set",
        "category": "entertainment",
        "price": 999,
        "rating": 4.7,
        "discount": 18,
        "platform": "Amazon",
        "emoji": "🎲"
    },

    {
        "name": "Return Gift Mini Hampers",
        "category": "gifts",
        "price": 1499,
        "rating": 4.4,
        "discount": 12,
        "platform": "Amazon",
        "emoji": "🎁"
    },

    {
        "name": "Veg Party Catering Package",
        "category": "food",
        "price": 299,
        "rating": 4.4,
        "discount": 0,
        "platform": "Swiggy",
        "emoji": "🍱",
        "unit": "per guest"
    },

    {
        "name": "Party Catering Package",
        "category": "food",
        "price": 349,
        "rating": 4.5,
        "discount": 0,
        "platform": "Zomato",
        "emoji": "🍛",
        "unit": "per guest"
    },

    {
        "name": "Budget Stay / Venue Search",
        "category": "venue",
        "price": 2499,
        "rating": 4.1,
        "discount": 10,
        "platform": "OYO",
        "emoji": "🏨",
        "unit": "starting"
    },

    {
        "name": "Pearl Drop Earrings",
        "category": "earrings",
        "price": 1299,
        "rating": 4.6,
        "discount": 25,
        "platform": "Amazon",
        "emoji": "💎"
    },

    {
        "name": "Gold-Tone Layered Necklace",
        "category": "necklace",
        "price": 1899,
        "rating": 4.5,
        "discount": 18,
        "platform": "Flipkart",
        "emoji": "📿"
    },

    {
        "name": "Minimal Kundan Set",
        "category": "jewelry set",
        "price": 2499,
        "rating": 4.7,
        "discount": 22,
        "platform": "Amazon",
        "emoji": "👑"
    },

    {
        "name": "Silver-Tone Bracelet",
        "category": "bracelet",
        "price": 999,
        "rating": 4.3,
        "discount": 15,
        "platform": "Flipkart",
        "emoji": "✨"
    },

    {
        "name": "Statement Jhumka Earrings",
        "category": "earrings",
        "price": 799,
        "rating": 4.5,
        "discount": 30,
        "platform": "Amazon",
        "emoji": "🌟"
    }
]


def product_link(item):

    platform = item["platform"]

    query = quote_plus(
        item["name"]
    )

    base = {

        "Amazon":
            f"https://www.amazon.in/s?k={query}",

        "Flipkart":
            f"https://www.flipkart.com/search?q={query}",

        "IKEA":
            f"https://www.ikea.com/in/en/search/?q={query}",

        "Swiggy":
            f"https://www.swiggy.com/search?query={query}",

        "Zomato":
            f"https://www.zomato.com/search?query={query}",

        "OYO":
            f"https://www.oyorooms.com/search?location={query}"
    }

    return base.get(
        platform,
        "#"
    )


def search_catalog(
    categories,
    budget,
    limit=8
):

    categories = {
        category.lower()
        for category in categories
    }

    matches = [
        item.copy()
        for item in CATALOG
        if item["category"].lower()
        in categories
    ]

    if not matches:

        matches = [
            item.copy()
            for item in CATALOG
        ]

    matches.sort(
        key=lambda item: (
            item["price"] > budget,
            -item["rating"],
            item["price"]
        )
    )

    for item in matches:

        item["url"] = product_link(
            item
        )

    return matches[:limit]