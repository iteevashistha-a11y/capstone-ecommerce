"""
Trovia Product Data Module
All product data used across the application
"""

PRODUCTS = [
    {
        "id": 1,
        "name": "iPhone 15",
        "category": "Electronics",
        "price": 79999,
        "rating": 4.5,
        "emoji": "📱",
        "description": "Apple iPhone 15 with A16 Bionic chip, 48MP camera, Dynamic Island, USB-C, and all-day battery life. Available in multiple colors.",
        "specs": {
            "Display": "6.1 inch Super Retina XDR",
            "Chip": "A16 Bionic",
            "Camera": "48MP Main + 12MP Ultra Wide",
            "Battery": "Up to 20 hours",
            "Storage": "128GB / 256GB / 512GB",
            "OS": "iOS 17"
        },
        "brand": "Apple",
        "in_stock": True,
        "tags": ["smartphone", "apple", "iphone", "mobile", "phone"],
        "image_keywords": ["phone", "smartphone", "mobile", "apple", "iphone"]
    },
    {
        "id": 2,
        "name": "Samsung TV 55\"",
        "category": "Electronics",
        "price": 54999,
        "rating": 4.3,
        "emoji": "📺",
        "description": "Samsung 55 inch 4K Crystal UHD Smart TV with Crystal Processor 4K, HDR, and Tizen OS for seamless streaming.",
        "specs": {
            "Size": "55 inches",
            "Resolution": "4K UHD (3840x2160)",
            "HDR": "HDR10+",
            "Smart TV": "Tizen OS",
            "Ports": "3x HDMI, 2x USB",
            "Refresh Rate": "60Hz"
        },
        "brand": "Samsung",
        "in_stock": True,
        "tags": ["tv", "television", "samsung", "4k", "smart tv"],
        "image_keywords": ["tv", "television", "screen", "monitor", "display"]
    },
    {
        "id": 3,
        "name": "Nike Air Max",
        "category": "Sports",
        "price": 8999,
        "rating": 4.6,
        "emoji": "👟",
        "description": "Nike Air Max running shoes with Max Air cushioning for all-day comfort. Breathable mesh upper, rubber outsole for grip.",
        "specs": {
            "Type": "Running / Casual",
            "Material": "Mesh + Synthetic",
            "Sole": "Rubber",
            "Cushioning": "Air Max",
            "Sizes": "UK 6-12",
            "Colors": "Black, White, Red"
        },
        "brand": "Nike",
        "in_stock": True,
        "tags": ["shoes", "nike", "sneakers", "running", "sports", "footwear"],
        "image_keywords": ["shoes", "sneakers", "footwear", "nike", "running shoes"]
    },
    {
        "id": 4,
        "name": "Levi's Jeans",
        "category": "Fashion",
        "price": 3499,
        "rating": 4.2,
        "emoji": "👖",
        "description": "Levi's 511 Slim Fit Jeans in classic blue denim. Comfortable stretch fabric, 5-pocket styling, durable construction.",
        "specs": {
            "Fit": "Slim Fit",
            "Material": "98% Cotton, 2% Elastane",
            "Rise": "Mid Rise",
            "Sizes": "28-40 waist",
            "Color": "Classic Blue, Black, Grey",
            "Care": "Machine Washable"
        },
        "brand": "Levi's",
        "in_stock": True,
        "tags": ["jeans", "denim", "levi's", "fashion", "clothing", "pants"],
        "image_keywords": ["jeans", "denim", "pants", "trousers", "clothing"]
    },
    {
        "id": 5,
        "name": "Harry Potter Set",
        "category": "Books",
        "price": 1299,
        "rating": 4.8,
        "emoji": "📚",
        "description": "Complete Harry Potter 7-book collection by J.K. Rowling. Box set includes all books from Philosopher's Stone to Deathly Hallows.",
        "specs": {
            "Books": "7 volumes",
            "Author": "J.K. Rowling",
            "Publisher": "Bloomsbury",
            "Format": "Paperback",
            "Language": "English",
            "Pages": "4100+ total"
        },
        "brand": "Bloomsbury",
        "in_stock": True,
        "tags": ["books", "harry potter", "fiction", "fantasy", "jk rowling"],
        "image_keywords": ["book", "books", "novel", "fiction", "reading"]
    },
    {
        "id": 6,
        "name": "Biryani Masala Kit",
        "category": "Food",
        "price": 599,
        "rating": 4.7,
        "emoji": "🍛",
        "description": "Authentic Hyderabadi Biryani Masala Kit with all spices and recipe card. Makes 5 servings of restaurant-style biryani.",
        "specs": {
            "Servings": "5 servings",
            "Includes": "Whole spices + Ground masala",
            "Shelf Life": "12 months",
            "Origin": "Hyderabad",
            "Organic": "Yes",
            "Weight": "250g"
        },
        "brand": "Shan",
        "in_stock": True,
        "tags": ["food", "biryani", "masala", "spices", "cooking", "indian food"],
        "image_keywords": ["food", "spices", "masala", "cooking", "indian food", "biryani"]
    },
    {
        "id": 7,
        "name": "Cricket Bat",
        "category": "Sports",
        "price": 2499,
        "rating": 4.4,
        "emoji": "🏏",
        "description": "SS Ton cricket bat made from Grade 1 English Willow. Professional grade bat with thick edges and perfect balance for power hitting.",
        "specs": {
            "Material": "Grade 1 English Willow",
            "Weight": "1.1-1.3 kg",
            "Handle": "Cane handle with grip",
            "Size": "Full size (Size 6)",
            "Grade": "Professional",
            "Brand": "SS Ton"
        },
        "brand": "SS Ton",
        "in_stock": True,
        "tags": ["cricket", "bat", "sports", "cricket bat", "willow"],
        "image_keywords": ["cricket", "bat", "sports equipment", "cricket bat"]
    },
    {
        "id": 8,
        "name": "Yoga Mat",
        "category": "Sports",
        "price": 899,
        "rating": 4.3,
        "emoji": "🧘",
        "description": "Premium non-slip yoga mat with alignment lines, 6mm thick for joint cushioning. Eco-friendly TPE material, includes carry strap.",
        "specs": {
            "Material": "Eco-friendly TPE",
            "Thickness": "6mm",
            "Size": "183cm x 61cm",
            "Features": "Non-slip, Alignment lines",
            "Weight": "1.2 kg",
            "Colors": "Purple, Blue, Green, Black"
        },
        "brand": "Boldfit",
        "in_stock": True,
        "tags": ["yoga", "mat", "fitness", "exercise", "sports", "gym"],
        "image_keywords": ["yoga mat", "mat", "exercise", "fitness", "yoga"]
    },
    {
        "id": 9,
        "name": "boAt Earbuds",
        "category": "Electronics",
        "price": 2999,
        "rating": 4.1,
        "emoji": "🎧",
        "description": "boAt Airdopes 141 True Wireless earbuds with 42Hr total playback, ENx Technology for clear calls, and IPX4 water resistance.",
        "specs": {
            "Type": "True Wireless",
            "Battery": "42 hours total",
            "Driver": "8mm",
            "Connectivity": "Bluetooth 5.1",
            "Water Resistance": "IPX4",
            "Microphone": "ENx Technology"
        },
        "brand": "boAt",
        "in_stock": True,
        "tags": ["earbuds", "wireless", "boat", "audio", "music", "tws"],
        "image_keywords": ["earbuds", "earphones", "headphones", "wireless audio", "tws"]
    },
    {
        "id": 10,
        "name": "Face Serum",
        "category": "Beauty",
        "price": 1499,
        "rating": 4.5,
        "emoji": "✨",
        "description": "Minimalist 10% Niacinamide Face Serum for pores, texture, and uneven skin tone. Dermatologist tested, suitable for all skin types.",
        "specs": {
            "Key Ingredient": "10% Niacinamide",
            "Volume": "30ml",
            "Skin Type": "All skin types",
            "Benefits": "Pores, Texture, Glow",
            "Fragrance": "Fragrance-free",
            "Tested": "Dermatologist tested"
        },
        "brand": "Minimalist",
        "in_stock": True,
        "tags": ["serum", "skincare", "beauty", "niacinamide", "face", "glow"],
        "image_keywords": ["serum", "skincare", "beauty product", "face cream", "cosmetics"]
    },
    {
        "id": 11,
        "name": "MacBook Air M2",
        "category": "Electronics",
        "price": 114999,
        "rating": 4.8,
        "emoji": "💻",
        "description": "Apple MacBook Air with M2 chip, 13.6-inch Liquid Retina display, 8GB RAM, 256GB SSD. Thin, light, and incredibly powerful.",
        "specs": {
            "Chip": "Apple M2",
            "Display": "13.6 inch Liquid Retina",
            "RAM": "8GB unified memory",
            "Storage": "256GB SSD",
            "Battery": "Up to 18 hours",
            "Weight": "1.24 kg"
        },
        "brand": "Apple",
        "in_stock": True,
        "tags": ["laptop", "macbook", "apple", "mac", "computer", "m2"],
        "image_keywords": ["laptop", "macbook", "computer", "apple laptop", "notebook"]
    },
    {
        "id": 12,
        "name": "Kurta Set",
        "category": "Fashion",
        "price": 1799,
        "rating": 4.3,
        "emoji": "👘",
        "description": "Elegant cotton kurta set with matching pyjama and dupatta. Traditional Indian ethnic wear perfect for festivals and casual outings.",
        "specs": {
            "Material": "Pure Cotton",
            "Set Includes": "Kurta + Pyjama + Dupatta",
            "Occasion": "Festive / Casual",
            "Sizes": "XS to 3XL",
            "Wash": "Machine washable",
            "Colors": "Blue, Pink, Green, Yellow"
        },
        "brand": "Fabindia",
        "in_stock": True,
        "tags": ["kurta", "ethnic", "traditional", "fashion", "indian wear", "festive"],
        "image_keywords": ["kurta", "ethnic wear", "indian clothing", "traditional dress", "salwar"]
    },
    {
        "id": 13,
        "name": "NCERT Books Set",
        "category": "Books",
        "price": 450,
        "rating": 4.6,
        "emoji": "📖",
        "description": "Complete NCERT Books Set for Class 10 - All subjects including Math, Science, Social Science, Hindi, and English.",
        "specs": {
            "Class": "Class 10",
            "Subjects": "All 5 subjects",
            "Publisher": "NCERT",
            "Format": "Paperback",
            "Language": "English + Hindi",
            "Edition": "Latest 2024"
        },
        "brand": "NCERT",
        "in_stock": True,
        "tags": ["books", "ncert", "textbooks", "class 10", "study", "education"],
        "image_keywords": ["textbook", "book", "study material", "academic", "education"]
    },
    {
        "id": 14,
        "name": "Instant Noodles Pack",
        "category": "Food",
        "price": 299,
        "rating": 4.0,
        "emoji": "🍜",
        "description": "Maggi 2-Minute Noodles pack of 12. The classic Indian instant noodles with masala seasoning. Quick, easy, and delicious.",
        "specs": {
            "Pack Size": "12 units x 70g",
            "Flavors": "Classic Masala",
            "Cook Time": "2 minutes",
            "Shelf Life": "9 months",
            "Origin": "India",
            "Brand": "Maggi"
        },
        "brand": "Maggi",
        "in_stock": True,
        "tags": ["noodles", "maggi", "instant food", "snacks", "food"],
        "image_keywords": ["noodles", "instant noodles", "food", "snack", "maggi"]
    },
    {
        "id": 15,
        "name": "Football",
        "category": "Sports",
        "price": 799,
        "rating": 4.2,
        "emoji": "⚽",
        "description": "Nivia Storm Football size 5, FIFA quality approved. Hand-stitched PU panels, butyl bladder for consistent air retention.",
        "specs": {
            "Size": "Size 5 (Standard)",
            "Material": "PU Panels",
            "Bladder": "Butyl",
            "Construction": "Hand-stitched",
            "Quality": "Match quality",
            "Brand": "Nivia"
        },
        "brand": "Nivia",
        "in_stock": True,
        "tags": ["football", "soccer", "sports", "ball", "outdoor"],
        "image_keywords": ["football", "soccer ball", "ball", "sports", "outdoor sports"]
    },
    {
        "id": 16,
        "name": "Lipstick Set",
        "category": "Beauty",
        "price": 999,
        "rating": 4.4,
        "emoji": "💄",
        "description": "Lakme 9to5 Matte Lipstick Set of 5 shades. Long-lasting matte formula, moisturizing, available in bold and nude shades.",
        "specs": {
            "Shades": "5 lipsticks",
            "Finish": "Matte",
            "Duration": "12 hours",
            "Formula": "Moisturizing",
            "Brand": "Lakme",
            "Skin Type": "All skin types"
        },
        "brand": "Lakme",
        "in_stock": True,
        "tags": ["lipstick", "makeup", "beauty", "cosmetics", "lakme", "lip color"],
        "image_keywords": ["lipstick", "makeup", "cosmetics", "beauty", "lip color"]
    },
    {
        "id": 17,
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "price": 3499,
        "rating": 4.5,
        "emoji": "🔊",
        "description": "JBL Go 3 portable Bluetooth speaker with bold JBL Original Pro Sound, waterproof (IPX67), and 5 hours playtime.",
        "specs": {
            "Brand": "JBL",
            "Battery": "5 hours playtime",
            "Connectivity": "Bluetooth 5.1",
            "Waterproof": "IPX67",
            "Weight": "209g",
            "Output": "4.2W RMS"
        },
        "brand": "JBL",
        "in_stock": True,
        "tags": ["speaker", "bluetooth", "jbl", "audio", "portable", "music"],
        "image_keywords": ["speaker", "bluetooth speaker", "audio device", "portable speaker", "music"]
    },
    {
        "id": 18,
        "name": "Saree",
        "category": "Fashion",
        "price": 4999,
        "rating": 4.6,
        "emoji": "🥻",
        "description": "Banarasi Silk Saree with golden zari work, rich border, and matching blouse piece. Perfect for weddings and special occasions.",
        "specs": {
            "Material": "Banarasi Silk",
            "Work": "Zari weaving",
            "Length": "6.3 meters + blouse",
            "Occasion": "Wedding / Festival",
            "Blouse": "Included",
            "Origin": "Varanasi"
        },
        "brand": "Nalli",
        "in_stock": True,
        "tags": ["saree", "silk", "banarasi", "ethnic", "wedding", "fashion", "indian"],
        "image_keywords": ["saree", "sari", "silk saree", "indian dress", "ethnic wear"]
    },
    {
        "id": 19,
        "name": "Python Programming Book",
        "category": "Books",
        "price": 549,
        "rating": 4.7,
        "emoji": "🐍",
        "description": "Python Crash Course by Eric Matthes - A hands-on, project-based introduction to Python programming for beginners.",
        "specs": {
            "Author": "Eric Matthes",
            "Publisher": "No Starch Press",
            "Pages": "544",
            "Format": "Paperback",
            "Level": "Beginner to Intermediate",
            "Edition": "3rd Edition"
        },
        "brand": "No Starch Press",
        "in_stock": True,
        "tags": ["python", "programming", "coding", "books", "technology", "computer"],
        "image_keywords": ["book", "programming book", "coding", "python", "computer science"]
    },
    {
        "id": 20,
        "name": "Protein Powder",
        "category": "Sports",
        "price": 2199,
        "rating": 4.1,
        "emoji": "💪",
        "description": "MuscleBlaze Whey Protein 1kg - 25g protein per serving, enriched with digestive enzymes, available in Chocolate and Vanilla.",
        "specs": {
            "Protein per serving": "25g",
            "Servings": "33 servings",
            "Weight": "1 kg",
            "Flavors": "Chocolate, Vanilla",
            "Type": "Whey Protein Concentrate",
            "Brand": "MuscleBlaze"
        },
        "brand": "MuscleBlaze",
        "in_stock": True,
        "tags": ["protein", "whey", "gym", "fitness", "supplements", "sports"],
        "image_keywords": ["protein powder", "supplement", "gym", "fitness", "whey protein"]
    }
]

CATEGORIES = [
    {"name": "Electronics", "emoji": "⚡", "description": "Phones, Laptops, TVs & more"},
    {"name": "Fashion", "emoji": "👗", "description": "Clothes, Shoes & Accessories"},
    {"name": "Books", "emoji": "📚", "description": "Fiction, Non-fiction & Textbooks"},
    {"name": "Food", "emoji": "🍽️", "description": "Groceries, Snacks & Beverages"},
    {"name": "Sports", "emoji": "🏆", "description": "Equipment, Gear & Apparel"},
    {"name": "Beauty", "emoji": "💅", "description": "Skincare, Makeup & Haircare"},
]

COUPON_CODES = {
    "SAVE10": {"type": "percent", "value": 10, "description": "10% off on all orders"},
    "FIRST50": {"type": "flat", "value": 50, "description": "Flat ₹50 off on first order"},
    "TROVIA20": {"type": "percent", "value": 20, "description": "20% off — Trovia special"},
}


def get_products_by_category(category):
    return [p for p in PRODUCTS if p["category"] == category]


def get_product_by_id(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def search_products(query):
    query = query.lower()
    results = []
    for p in PRODUCTS:
        if (query in p["name"].lower() or
                query in p["description"].lower() or
                query in p["category"].lower() or
                any(query in tag for tag in p["tags"])):
            results.append(p)
    return results


def get_featured_products(count=6):
    featured = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)
    return featured[:count]


def get_trending_products(count=4):
    trending = sorted(PRODUCTS, key=lambda x: x["price"], reverse=True)
    return trending[:count]
