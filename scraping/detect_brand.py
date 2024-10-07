import json

brand_map = {
    # Nike
    "Air": "Nike", "Jordan": "Nike", "Air Max": "Nike", "Dunk": "Nike",
    "Blazer": "Nike", "Force": "Nike", "Vapor": "Nike", "React": "Nike",
    "Pegasus": "Nike", "Zoom": "Nike", "Cortez": "Nike", "NikeLab": "Nike",
    "Kobe": "Nike", "Quest": "Nike", "Sabrina": "Nike", "Metcon": "Nike",
    "Clogposite": "Nike", "LeBron": "Nike", "Alpha": "Nike", "Gore-Tex": "Nike",
    "Structure": "Nike", "Infinity Run": "Nike", "Phantom": "Nike", "Presto": "Nike",
    "Flyknit": "Nike", "Huarache": "Nike", "Free": "Nike", "ACG": "Nike",
    "Shox": "Nike", "Air Rift": "Nike", "Hyperdunk": "Nike", "Odyssey": "Nike",
    "Epic": "Nike", "Mercurial": "Nike", "Tiempo": "Nike", "M2K Tekno": "Nike",
    "Daybreak": "Nike", "Waffle": "Nike", "Killshot": "Nike", "FlyEase": "Nike",
    "React Element": "Nike", "Roshe": "Nike", "Crater": "Nike", "SFB": "Nike",
    "Fear of God": "Nike", "Waffle One": "Nike", "ISPA": "Nike", "Court Vision": "Nike",
    "Sb" : "Nike", "Lunar" : "Nike",

    # Adidas
    "UltraBoost": "Adidas", "Yeezy": "Adidas", "NMD": "Adidas", "Superstar": "Adidas",
    "Stan Smith": "Adidas", "Gazelle": "Adidas", "Samba": "Adidas", "Adizero": "Adidas",
    "Predator": "Adidas", "Copa": "Adidas", "X": "Adidas", "Pharrell": "Adidas",
    "ZX": "Adidas", "Forum": "Adidas", "EQT": "Adidas", "Ozweego": "Adidas",
    "SL": "Adidas", "Terrex": "Adidas", "Torsion": "Adidas", "Tubular": "Adidas",
    "4D": "Adidas", "Alphabounce": "Adidas", "Climacool": "Adidas", "POD": "Adidas",
    "Crazy Explosive": "Adidas", "PureBoost": "Adidas", "Nite Jogger": "Adidas",
    "Prophere": "Adidas", "Falcon": "Adidas", "Iniki": "Adidas", "Raf Simons": "Adidas",

    # Puma
    "Suede": "Puma", "RS-X": "Puma", "Rider": "Puma", "Cali": "Puma",
    "Basket": "Puma", "Cell": "Puma", "Disc": "Puma", "Future Rider": "Puma",
    "Fenty": "Puma", "Ignite": "Puma", "Evoknit": "Puma", "Tsugi": "Puma",
    "Roma": "Puma", "Speedcat": "Puma", "RS Dreamer": "Puma", "Slipstream": "Puma",
    "Blaze": "Puma", "Jamming": "Puma", "Avid": "Puma", "Ralph Sampson": "Puma",
    "LQDCell": "Puma", "Thunder": "Puma", "Wild Rider": "Puma", "Clyde": "Puma",

    # New Balance
    "574": "New Balance", "990": "New Balance", "997": "New Balance",
    "550": "New Balance", "9060": "New Balance", "X-Racer": "New Balance",
    "Hesi Low": "New Balance", "1080": "New Balance", "860": "New Balance",
    "Fresh Foam": "New Balance", "FuelCell": "New Balance", "Kaizen": "New Balance",
    "998": "New Balance", "373": "New Balance", "327": "New Balance",
    "Vision Racer": "New Balance", "2002R": "New Balance", "501": "New Balance",
    "Vongo": "New Balance", "Minimus": "New Balance", "Cush+": "New Balance","1000" : "New Balance",
    "1906A" : "New Balance",

    # Skechers
    "D'Lites": "Skechers", "Max Cushioning": "Skechers", "Go Walk": "Skechers",
    "Arch Fit": "Skechers", "Energy": "Skechers", "Skech-Air": "Skechers",
    "GOrun": "Skechers", "Bobs": "Skechers", "Flex Appeal": "Skechers",
    "Gowalk Arch": "Skechers", "Hyper Burst": "Skechers", "Ultra Flex": "Skechers",
    "D'Lux": "Skechers", "You by Skechers": "Skechers", "Skechers Foamies": "Skechers",
    "Twinkle Toes": "Skechers", "Relaxed Fit": "Skechers", "Equalizer": "Skechers",
    "Shuffles": "Skechers", "Treadfit": "Skechers", "Delson": "Skechers",

    # Asics
    "Gel": "Asics", "Kayano": "Asics", "Nimbus": "Asics", "Cumulus": "Asics",
    "Quantum": "Asics", "Lyte": "Asics", "Noosa": "Asics", "GT-2000": "Asics",
    "GT-1000": "Asics", "Trabuco": "Asics", "Metaride": "Asics", "Tarther": "Asics",
    "DS Trainer": "Asics", "Gel-Lyte III": "Asics", "Gel-Venture": "Asics",
    "FujiTrabuco": "Asics", "GlideRide": "Asics", "Court FF": "Asics", "Blast": "Asics",
    "Kihachiro": "Asics"
}

def extract_brand(slug):
    for key, brand in brand_map.items():
        if str(key).lower() in str(slug).lower():
            return brand
    return "Unknown"

with open('data/sneakers_data_v1.json', 'r') as file:
    data = json.load(file)

count = 0
for sneaker in data:
    name = sneaker.get('value')
    #print(slug)
    brand = extract_brand(name)
    if str(brand) != "Unknown":
        count += 1
    sneaker["brand"] = brand

with open('updated_sneaker_data.json', 'w') as file:
    json.dump(data, file, indent=4)

print(count)
